"""
================================================================================
16. COMMON INTERVIEW QUESTIONS & ANSWERS
================================================================================

API & Semantics
---------------

Q: How exactly would your API look for ingesting events (start, ping, end)?
A: We use REST API for event ingestion:
   - Endpoint: POST /v1/events
   - Request body: {job_id, event_type (start/ping/end), timestamp, 
     timeout_seconds, metadata}
   - Response: 202 Accepted with event_id and partition_id
   See Section 3 for full API specification.

Q: Would you use REST endpoint, gRPC, or streaming API like Kafka?
A: Hybrid approach:
   - REST API for client ingestion (simple, widely compatible)
   - Kafka internally for event processing (ordering, scalability, replay)
   - WebSocket for streaming timeout notifications to scheduler
   REST provides simplicity for clients, Kafka provides durability and 
   partitioning for internal processing.

Q: What happens if two events for the same job arrive out of order?
A: Last-write-wins based on timestamp:
   - Check if incoming timestamp > stored last_seen
   - If yes: apply update
   - If no: log out-of-order event but don't update state
   - Event history stored separately for audit
   This prevents old events from overwriting newer state. See Section 4.

Q: How would you expose an API to query currently active jobs?
A: Multiple options:
   - Snapshot: GET /v1/jobs/active (returns paginated list)
   - Specific job: GET /v1/jobs/{job_id}
   - Streaming: WebSocket /v1/stream/timeouts (real-time timeout notifications)
   - Historical: GET /v1/jobs/timeouts?since=<timestamp>
   See Section 3 for complete query API design.


Timeout Detection
-----------------

Q: With millions of jobs with varying timeouts, how would you efficiently 
   detect timeouts?
A: Hybrid approach combining three strategies:
   1. Timer wheel (primary): O(1) insertion/deletion, circular buffer with 
      3600 slots (1 second granularity). Jobs distributed across slots by 
      expiry time. Check current slot every second.
   2. Periodic sweep (backup): Every 60 seconds, scan Redis sorted set for 
      jobs past timeout. Catches missed timeouts from crashes or bugs.
   3. Event-driven: Remove jobs from timeout candidates immediately when 
      ping/end events arrive.
   
   For 1M active jobs with timer wheel:
   - Average 300 jobs per slot checked each second
   - O(1) complexity per job update
   - Much more efficient than heap (O(log N)) or full scan (O(N))
   See Section 5 for detailed implementation.

Q: How would you avoid false positives if the event stream is delayed?
A: Multiple safeguards:
   - Use event timestamp (not receive time) for last_seen calculation
   - Periodic sweep verifies timer wheel results before marking timeout
   - Monitor event processing lag; alert if lag > 60 seconds
   - During high lag, we can temporarily increase timeout thresholds
   - Idempotent timeout processing: if ping arrives after timeout detected, 
     we can reverse the timeout decision

Q: Can timeouts be dynamic per job? If so, how do you track that efficiently?
A: Yes, per-job dynamic timeouts:
   - Each job stores its own timeout_seconds in state (both Redis and Postgres)
   - Passed in every event (start/ping) so workers can change it mid-execution
   - Timer wheel expiry slot calculated as: (current_time + job.timeout) % 3600
   - On timeout value change: remove from old slot, insert into new slot (O(1))
   - No global timeout configuration needed
   See Section 2 for job state structure.


Scalability & Fault Tolerance
------------------------------

Q: How do you partition jobs across multiple servers so no single server tracks 
   all jobs?
A: Partition by job_id using consistent hashing:
   - Hash(job_id) % num_partitions determines target partition
   - Each partition has dedicated: event processor, timeout checker, Redis shard
   - Use 100-150 virtual nodes per physical partition for load balancing
   - Events routed to correct partition via Kafka partition key (job_id)
   - Typical deployment: 50-100 partitions for 10M+ jobs
   
   Sizing:
   - Each processor handles 10K events/sec
   - Each Redis instance handles 1M active jobs
   - Each timer wheel handles 100K jobs efficiently
   See Section 6 for partitioning strategy.

Q: What happens if the server tracking a partition crashes?
A: Multi-layer recovery:
   1. Event processor crash:
      - Kafka consumer group rebalances within 10 seconds
      - New processor resumes from last committed offset
      - WAL replay ensures no state updates lost
   
   2. Timeout checker crash:
      - Leader election promotes new leader within 5 seconds
      - New leader rebuilds timer wheel from Redis (10-30 seconds for 1M jobs)
      - During rebuild: periodic sweep acts as backup
   
   3. Redis crash:
      - Redis Sentinel/Cluster promotes replica within seconds
      - AOF persistence minimizes data loss
      - Event replay from Kafka if needed
   
   No timeouts are lost because:
   - Events in Kafka (durable, can replay)
   - State in Redis (replicated)
   - Periodic sweep catches any missed timeouts
   See Section 9 for complete recovery procedures.

Q: How would you replicate state across multiple nodes to prevent data loss?
A: Multi-tier replication:
   
   Hot state (Redis):
   - Redis Cluster with replication factor of 3
   - Writes to primary, replicate to 2 replicas
   - AOF (Append-Only File) for durability
   - Automatic failover within seconds
   
   Cold state (Postgres):
   - Streaming replication with synchronous commit
   - At least 1 replica before acknowledging writes
   - Read replicas for query offloading
   
   Event stream (Kafka):
   - Replication factor of 3
   - Min in-sync replicas of 2
   - Events stored durably, can replay
   
   Application layer:
   - Write-Ahead Log (WAL) on event processors
   - Uncommitted WAL entries replayed on crash
   See Section 7 for fault tolerance details.


Data Storage
------------

Q: What data do you need to persist long-term vs. what can remain in memory?
A: Three-tier storage strategy:
   
   Memory only (hot path):
   - Local LRU cache on processors: Recently accessed jobs (100K capacity, 
     1-min TTL)
   - Bloom filter: Job existence checks (20 MB for 10M jobs)
   - Timer wheel: Active timeout tracking (just pointers, minimal memory)
   
   Redis (hot storage, short-term persistence):
   - Active jobs: Full state with TTL (timeout + 2 min buffer)
   - Recently completed jobs: 1-min grace period
   - Deduplication cache: 5-min sliding window
   - Active job indices: Sorted sets by last_seen
   - Why Redis: Sub-millisecond access, sorted sets for range queries
   
   Postgres (cold storage, long-term persistence):
   - Completed jobs: 30-day retention
   - Timed-out jobs: Historical analysis
   - Job events: Audit trail, partitioned by date
   - Why Postgres: ACID guarantees, complex queries, cost-effective for cold data
   
   Trade-off: Redis provides speed for real-time operations, Postgres provides 
   durability for historical analysis. See Section 2.

Q: How would you handle queries like "Show all jobs that timed out in the last 
   24 hours"?
A: Multi-level query strategy:
   
   Recent timeouts (< 1 hour):
   - Query Redis sorted set per partition
   - Key: "jobs:timeout:partition:{N}"
   - Range query by timestamp (ZRANGEBYSCORE)
   - Fan out to all partitions in parallel
   - Merge results: ~50ms total
   
   Historical timeouts (1-24 hours):
   - Query Postgres jobs table
   - WHERE status='timed-out' AND last_seen >= NOW() - INTERVAL '24 hours'
   - Table partitioned by day for fast scans
   - B-tree index on (status, last_seen)
   - Result: ~50ms with proper indexing
   
   Optimization:
   - Cache frequent queries (e.g., "last 1 hour") in Redis
   - Pre-aggregate timeout counts per hour
   - Use read replicas to offload primary
   See Section 3 for query APIs and Section 8 for optimizations.


Distributed Scheduling Angle
-----------------------------

Q: How do you ensure fairness if multiple tenants submit jobs?
A: Multi-tenant fairness with quotas:
   
   Per-tenant limits:
   - Max concurrent jobs: 1,000 per tenant
   - Rate limit: 100 job starts per minute per tenant
   - Tracked in Redis: "jobs:active:tenant:{tenant_id}"
   
   Scheduler strategy:
   - Weighted fair queuing: Each tenant gets share proportional to quota
   - Within tenant: Priority-based or FIFO
   - Separate queues per tenant to prevent head-of-line blocking
   
   Job monitor support:
   - Query API filters by tenant_id
   - Exposes per-tenant active job counts
   - Aggregates: GET /v1/stats/active returns per-tenant counts
   
   Prevents monopolization while maintaining isolation. See Section 11.

Q: What retry policy would you support for failed jobs?
A: Configurable exponential backoff:
   
   Configuration per job:
   - max_retries: 3 (stored in metadata)
   - initial_delay: 5 seconds
   - backoff_multiplier: 2
   - max_delay: 300 seconds (5 minutes)
   - jitter: ±20% to prevent thundering herd
   
   Retry logic:
   - On timeout: check current_retry_count < max_retries
   - If yes: delay = min(initial_delay * 2^current_retry_count + jitter, max_delay)
   - Requeue job after delay with incremented retry count
   - If no retries remain: mark as permanently failed
   
   Implementation:
   - Retry events are new start events with same job_id, new attempt_id
   - Job monitor tracks both for correlation
   - Timeouts apply per attempt, not cumulative
   
   Example progression: 5s → 10s → 20s → failed
   See Section 11 for retry policies.

Q: How would you handle idempotency in job submission and event ingestion?
A: Multiple idempotency layers:
   
   Event ingestion:
   - Deduplication key: job_id + timestamp
   - Two-phase check:
     1. Bloom filter (5-min window): Fast probabilistic check
     2. Redis dedup cache: Exact check with key "dedup:{job_id}:{timestamp}", 
        5-min TTL
   - If duplicate: acknowledge but skip processing
   - False positive rate: 0.1%
   
   State updates:
   - Last-write-wins based on timestamp prevents out-of-order issues
   - Idempotent operations: Setting status=completed multiple times has same effect
   - Job_id uniqueness enforced: Resubmitting same job_id updates existing job
   
   Kafka consumption:
   - At-least-once delivery: Events may be reprocessed on crash
   - Idempotent state updates ensure correctness
   - Offset commits after successful state update
   
   Client retries:
   - Clients can safely retry on 503/timeout
   - Same event_id in response allows correlation
   - Duplicate events filtered by deduplication logic
   See Section 4 for deduplication strategy.


Optimization / Edge Cases
--------------------------

Q: What happens if a job never sends an end event? Do you keep it in memory 
   forever?
A: Multiple safeguards against memory leaks:
   
   Redis TTL:
   - Every job has TTL = timeout + 2-minute buffer
   - Automatically evicted from Redis after TTL expires
   - Even if no end event arrives, job is removed from hot storage
   
   Timeout detection:
   - If no ping within timeout period, job times out
   - Timeout processing removes from active sets
   - State persisted to Postgres as timed-out
   
   Periodic cleanup:
   - Periodic sweep (every 60 seconds) catches stale jobs
   - Jobs with expired TTL removed from timer wheel
   - Postgres cold storage has retention policy (e.g., 30 days)
   
   Worst case:
   - Job stays in Redis for timeout + 2 minutes
   - Job stays in timer wheel until timeout
   - Then automatically cleaned up
   - Memory impact: ~1 KB per job
   See Section 2 for TTL strategy and Section 5 for timeout detection.

Q: If a worker machine restarts, how do you reschedule jobs that were running 
   there?
A: Scheduler-driven rescheduling:
   
   Detection:
   1. Worker stops sending pings (every 30 seconds)
   2. After timeout (e.g., 5 minutes), job monitor detects timeout
   3. Timeout event published to WebSocket /v1/stream/timeouts
   4. Scheduler receives timeout notification
   
   Rescheduling:
   1. Scheduler checks retry policy: current_retry_count < max_retries
   2. If retries remain:
      - Requeue job with exponential backoff delay
      - New start event with same job_id, new attempt_id
      - Different worker picks up the job
   3. If no retries remain: mark as permanently failed
   
   Worker restart scenarios:
   - Graceful shutdown: Worker sends end events before stopping
   - Crash: Jobs timeout after 5 minutes, then retry
   - Network partition: May spuriously timeout, but corrected when partition heals
   
   Optimization:
   - Scheduler can track worker health separately
   - On worker crash detection, proactively requeue all jobs from that worker
   - Faster than waiting for individual timeouts
   See Section 11 for scheduler integration and Section 12 for edge cases.

Q: How would you minimize latency when detecting timeouts in high-load conditions?
A: Multi-pronged optimization strategy:
   
   Timer wheel efficiency:
   - O(1) insertion/deletion even under load
   - Only check current slot (typically 300 jobs/sec for 1M jobs)
   - No need to scan entire job set
   
   Partitioning for parallelism:
   - 100 partitions = 100 independent timeout checkers
   - Each processes 1/100th of the jobs
   - Linear scalability with partition count
   
   Local caching:
   - 100K-job LRU cache per processor
   - 70-80% cache hit rate
   - Reduces Redis round trips from 100% to 20%
   - Latency: 0.1ms (cache) vs 2ms (Redis)
   
   Batch processing:
   - Batch 100 events or 100ms worth before flushing
   - Reduces write amplification by 100x
   - Redis pipelining: Multiple commands in one round trip
   
   Backpressure handling:
   - Return 503 when Kafka queue depth > 100K messages
   - Clients implement exponential backoff
   - Prioritize ping/end events over start events
   
   Resource optimization:
   - Read replicas for queries (offload primary)
   - Bloom filter for non-existent jobs (skip lookups)
   - Windowed indexes in Postgres (scan only relevant partitions)
   
   Result: Sub-second timeout detection even at 1M events/sec. See Section 8 
   for performance optimizations.


================================================================================
                    JOB MONITORING SYSTEM - COMPLETE FLOW
================================================================================

COMPONENTS OVERVIEW:
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  ┌──────────┐      ┌──────────┐      ┌───────────────┐                    │
│  │ WORKERS  │      │   API    │      │     KAFKA     │                     │
│  │          │      │ GATEWAY  │      │  (Message     │                     │
│  │ Doing    │─────▶│          │─────▶│   Queue)      │                     │
│  │ actual   │      │ /v1/     │      │               │                     │
│  │ work     │      │ events   │      │ Durable       │                     │
│  └──────────┘      └──────────┘      │ Storage       │                     │
│                                        └───────┬───────┘                     │
│                                                │                             │
│                                                ▼                             │
│                                        ┌───────────────┐                    │
│                                        │    EVENT      │                     │
│                                        │  PROCESSOR    │                     │
│                                        │  (Reads from  │                     │
│                                        │   Kafka)      │                     │
│                                        └───────┬───────┘                     │
│                                                │                             │
│                          ┌─────────────────────┼─────────────────┐          │
│                          ▼                     ▼                 ▼          │
│                    ┌──────────┐         ┌──────────┐      ┌──────────┐    │
│                    │  REDIS   │         │ POSTGRES │      │  TIMER   │    │
│                    │  (Fast   │         │ (Durable │      │  WHEEL   │    │
│                    │  Cache)  │         │  History)│      │ (Timeout │    │
│                    │          │         │          │      │  Check)  │    │
│                    └──────────┘         └──────────┘      └────┬─────┘    │
│                                                                  │          │
│                                                                  ▼          │
│                                                            ┌──────────┐    │
│                                                            │SCHEDULER │    │
│                                                            │ (Retries)│    │
│                                                            └──────────┘    │
└────────────────────────────────────────────────────────────────────────────┘


================================================================================
                        SCENARIO 1: JOB STARTS
================================================================================

┌─────────────┐
│   WORKER    │  "I'm starting to process a video"
│  (Machine   │  
│  doing work)│  
└──────┬──────┘
       │ 1. POST /v1/events
       │    {
       │      job_id: "video-123",
       │      event_type: "start",
       │      timestamp: "10:00:00",
       │      timeout_seconds: 300  (5 minutes)
       │    }
       ▼
┌─────────────┐
│  REST API   │  2. Validates request
│             │  3. Returns 202 Accepted immediately (1ms)
└──────┬──────┘
       │ 4. Publishes to Kafka
       │    (Event now safe on disk, replicated 3x)
       ▼
┌─────────────┐
│   KAFKA     │  5. Stores event durably
│  (Message   │     - Partition by job_id
│   Queue)    │     - Will not lose even if server crashes
└──────┬──────┘
       │ 6. Event Processor reads
       ▼
┌─────────────┐
│   EVENT     │  7. Processes event:
│  PROCESSOR  │     - Check if duplicate (no)
│             │     - Create job entry
└──────┬──────┘
       │ 8. Updates storage
       │
   ┌───┴───────────────┐
   │                   │
   ▼                   ▼
┌─────────┐      ┌──────────┐      ┌────────────┐
│ REDIS   │      │ POSTGRES │      │ TIMER      │
│         │      │          │      │ WHEEL      │
│ Key:    │      │ INSERT:  │      │            │
│ job:    │      │ job_id   │      │ Slot 300:  │
│ video-  │      │ status   │      │ [video-123]│
│ 123     │      │ created  │      │ (expires   │
│         │      │ last_seen│      │  in 5 min) │
│ Value:  │      │          │      │            │
│ {       │      │          │      │ Every 1sec │
│  status:│      │          │      │ check this │
│  "active│      │          │      │ slot       │
│  last_  │      │          │      │            │
│  seen:  │      │          │      │            │
│  10:00  │      │          │      │            │
│  timeout│      │          │      │            │
│  300s   │      │          │      │            │
│ }       │      │          │      │            │
└─────────┘      └──────────┘      └────────────┘
  ↑                                      ↑
  │                                      │
  Fast (1-2ms)                    Checks for timeouts
  For queries                     every second


================================================================================
                    SCENARIO 2: JOB SENDS PING (HEARTBEAT)
================================================================================

Time: 10:01:00 (1 minute later)

┌─────────────┐
│   WORKER    │  "Still working on video-123!"
└──────┬──────┘
       │ 1. POST /v1/events
       │    {
       │      job_id: "video-123",
       │      event_type: "ping",
       │      timestamp: "10:01:00"
       │    }
       ▼
┌─────────────┐
│  REST API   │  2. Returns 202 (fast!)
└──────┬──────┘
       │ 3. To Kafka
       ▼
┌─────────────┐
│   KAFKA     │
└──────┬──────┘
       │ 4. Event Processor reads
       ▼
┌─────────────┐
│   EVENT     │  5. Check duplicate? No.
│  PROCESSOR  │  6. Compare timestamps:
│             │     Current last_seen: 10:00:00
│             │     New timestamp:     10:01:00
│             │     10:01:00 > 10:00:00 ✓
│             │     → UPDATE!
└──────┬──────┘
       │
   ┌───┴───────────────┐
   │                   │
   ▼                   ▼
┌─────────┐      ┌──────────┐      ┌────────────┐
│ REDIS   │      │ POSTGRES │      │ TIMER      │
│         │      │          │      │ WHEEL      │
│ UPDATE: │      │ UPDATE:  │      │            │
│         │      │ last_seen│      │ MOVE job   │
│ last_   │      │ = 10:01  │      │ from slot  │
│ seen:   │      │          │      │ 300 to     │
│ 10:01   │      │          │      │ slot 360   │
│ (was    │      │          │      │            │
│  10:00) │      │          │      │ [video-123]│
│         │      │          │      │ now expires│
│ Refresh │      │          │      │ at 10:06:00│
│ TTL     │      │          │      │ (5 min from│
│         │      │          │      │  now)      │
└─────────┘      └──────────┘      └────────────┘

Result: System knows job is still alive! ✓


================================================================================
              SCENARIO 3: JOB CRASHES (NO MORE PINGS)
================================================================================

Time: 10:02:00 - Worker crashes! 💥

┌─────────────┐
│   WORKER    │  💥 CRASH!
│   (DEAD)    │  No more pings sent...
└─────────────┘
       │
       X (no communication)
       

10:02:00 - Last ping was at 10:01:00
10:03:00 - No ping (1 min since last ping)
10:04:00 - No ping (2 min since last ping)
10:05:00 - No ping (3 min since last ping)
10:06:00 - No ping (4 min since last ping)
10:07:00 - No ping (5 min since last ping) ⚠️

┌────────────┐
│ TIMER      │  Every 1 second, checking:
│ WHEEL      │
│            │  Time: 10:06:01
│ Slot 360:  │  Check slot 360
│ [video-123]│  Found: video-123
│            │  
│ CHECK:     │  Job expiry time: 10:06:00
│ now = 10:  │  Current time:    10:06:01
│ 06:01      │  
│            │  10:06:01 >= 10:06:00 → TIMEOUT! ⚠️
│ expiry =   │
│ 10:06:00   │
│            │  1. Mark as "timed-out"
│ TIMED OUT! │  2. Remove from active jobs
└─────┬──────┘  3. Publish timeout event
      │
      ▼
┌─────────────┐
│ SCHEDULER   │  4. Receives timeout notification:
│             │     "video-123 timed out!"
│             │  
│ Action:     │  5. Check retry policy:
│ - Retry job │     current_retry = 0
│   on new    │     max_retries = 3
│   worker    │     → Can retry!
│             │
│ - Create    │  6. Requeue job:
│   new start │     POST /v1/events
│   event     │     {
│             │       job_id: "video-123",
│             │       event_type: "start",
│             │       attempt: 2
└─────────────┘     }

                 7. New worker picks up job
                 8. Process repeats!


================================================================================
                    SCENARIO 4: OUT-OF-ORDER EVENTS
================================================================================

Network reorders packets!

┌─────────────┐
│   WORKER    │  Sends in order:
│             │  1. Ping at T=10:01:00
│             │  2. Ping at T=10:02:00
└──────┬──────┘  3. Ping at T=10:03:00
       │
       │ Network delay/reordering
       │
       ▼
┌─────────────┐  Receives in order:
│  REST API   │  1. Ping at T=10:02:00 ✓
│             │  2. Ping at T=10:03:00 ✓  
│             │  3. Ping at T=10:01:00 ⚠️ (late!)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   EVENT     │  Processing:
│  PROCESSOR  │  
│             │  Event 1 (T=10:02:00):
│             │  current last_seen = 10:00:00
│             │  10:02:00 > 10:00:00 ✓
│             │  → Update to 10:02:00
│             │
│             │  Event 2 (T=10:03:00):
│             │  current last_seen = 10:02:00
│             │  10:03:00 > 10:02:00 ✓
│             │  → Update to 10:03:00
│             │
│             │  Event 3 (T=10:01:00):
│             │  current last_seen = 10:03:00
│             │  10:01:00 > 10:03:00 ✗
│             │  → DON'T update!
│             │  → Log as out-of-order
│             │  → Still save to history table
└─────────────┘
       │
       ▼
┌─────────────┐      ┌──────────────┐
│   REDIS     │      │  POSTGRES    │
│             │      │  history     │
│ last_seen:  │      │              │
│ 10:03:00    │      │ All events:  │
│ (correct!)  │      │ T=10:02:00 ✓ │
│             │      │ T=10:03:00 ✓ │
│             │      │ T=10:01:00 ✓ │
│             │      │ (audit trail)│
└─────────────┘      └──────────────┘


================================================================================
                        WHY EACH COMPONENT?
================================================================================

┌─────────────────────────────────────────────────────────────────────────┐
│ REST API                                                                 │
│ Why: Workers speak HTTP (universal, simple)                             │
│ Fast: Returns in <1ms                                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ KAFKA                                                                    │
│ Why: Durable storage that never loses events                            │
│ Benefit: Can replay if needed, survives crashes                         │
│ Fast: Async processing, don't block clients                             │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ EVENT PROCESSOR                                                          │
│ Why: Separates receiving from processing                                │
│ Benefit: Can crash and restart without losing data                      │
│ Scalable: Run 100 processors in parallel                                │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ REDIS (Hot Storage)                                                      │
│ Why: Fast queries (1-2ms vs 50ms for Postgres)                         │
│ What: Active jobs only, with TTL                                        │
│ Trade-off: Expensive but necessary for speed                            │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ POSTGRES (Cold Storage)                                                  │
│ Why: Durable long-term history                                          │
│ What: All completed/timed-out jobs                                      │
│ Trade-off: Slower but cheap and reliable                                │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ TIMER WHEEL                                                              │
│ Why: Efficient timeout checking (O(1) not O(N))                        │
│ What: Circular buffer with 3600 slots (1 per second)                   │
│ Benefit: Check 300 jobs/sec instead of 5 million/sec                   │
└─────────────────────────────────────────────────────────────────────────┘


================================================================================
                    KEY NUMBERS (For Interview)
================================================================================

Scale:
- 5 million active jobs
- 166,000 pings/second (5M jobs × ping every 30s)
- Sub-second timeout detection required

Latencies:
- REST API response: <1ms
- Redis read/write: 1-2ms
- Postgres read/write: 10-50ms
- Kafka publish: 1-5ms
- Timeout detection: <1 second after timeout

Storage:
- Redis: ~500 bytes per job × 5M jobs = 2.5 GB
- Postgres: Historical data (30 day retention)
- Kafka: Events for last 7 days (for replay)

Partitioning:
- 100 partitions
- Each handles 50,000 jobs
- Each processes 1,660 events/sec
- Independent failure domains

KEY DATA FLOWS:
1. Worker → API → Kafka → Processor → Redis/Postgres
2. Processor → Redis → Timeout Checker → WebSocket → Scheduler
3. Query: Client → API → Redis (hot) / Postgres (cold) → Response

MONITORING:
- Prometheus/Grafana for metrics
- OpenTelemetry for distributed tracing
- Structured logs with job_id + partition_id
- Alerting on p99 latency, partition lag, timeout detection latency


================================================================================
17. INTERVIEW WALKTHROUGH SCRIPT (Start to Finish)
================================================================================

This is the narrative flow to present the design in an interview. Follow this 
structure to tell a coherent story.

STEP 1: Understand the Problem
-------------------------------
"Let me start by clarifying the requirements. We're building a job monitoring 
system that tracks millions of long-running jobs. Workers send periodic heartbeats 
(pings), and we need to detect when jobs stop responding within their timeout 
period. The system needs to handle millions of events per second and detect 
timeouts within seconds, not minutes."

Key requirements:
- High throughput: millions of events/sec
- Sub-second timeout detection
- Millions of concurrent jobs
- Must survive crashes without losing timeouts


STEP 2: Start with the Data Model
----------------------------------
"First, let me define what we're tracking for each job."

DECISION: Per-job state structure
{
  job_id: unique identifier
  status: active | completed | timed-out
  last_seen: timestamp of most recent ping
  first_seen: when job started
  timeout_seconds: how long before timeout
  metadata: priority, owner, etc.
}

WHY: We need just enough information to detect timeouts (last_seen + timeout) 
and support queries. Keeping it minimal reduces memory footprint.

PROBLEM IT SOLVES: With millions of jobs, every byte matters. ~500 bytes per 
job means 1M jobs = 500MB, which is manageable.


STEP 3: Choose Storage Strategy
--------------------------------
"Not all jobs need the same treatment. Active jobs need fast access, completed 
jobs can be cold storage."

DECISION: Three-tier storage
- Memory (local cache): 100K most recent jobs, sub-millisecond access
- Redis: Active jobs only, 1-2ms access
- Postgres: Completed/timed-out jobs, historical queries

WHY: Trading off speed vs cost. Redis is expensive at scale, Postgres is cheap 
but slower. Keep hot data hot, cold data cold.

PROBLEM IT SOLVES: If we kept everything in Redis, we'd need massive memory. 
If we used only Postgres, queries would be too slow. This gives us both speed 
and cost-efficiency.


STEP 4: API Design for Event Ingestion
---------------------------------------
"Workers need to send job events - start, ping, end."

DECISION: REST API for client ingestion
POST /v1/events
{job_id, event_type, timestamp, timeout_seconds}
→ Returns 202 Accepted

WHY: REST is simple and universal. Every language has HTTP clients. We accept 
immediately (202) and process async for low latency.

PROBLEM IT SOLVES: Blocking on storage writes would add 10-50ms latency. Async 
processing keeps ingestion fast (<1ms) while still ensuring durability through 
Kafka.


STEP 5: Internal Event Processing with Kafka
---------------------------------------------
"Between ingestion and state updates, we need ordering and durability."

DECISION: Use Kafka as internal event bus
- API publishes to Kafka topic "job-events"
- Partition key = job_id for ordering
- Event processors consume and update state

WHY: Kafka gives us three critical properties:
1. Ordering: All events for same job_id go to same partition
2. Durability: Can replay after crashes
3. Scalability: Parallel consumption across partitions

PROBLEM IT SOLVES: If processors crash, events aren't lost - they're in Kafka. 
When processor restarts, it resumes from last offset. No data loss.


STEP 6: Handle Out-of-Order Events
-----------------------------------
"Networks reorder packets. Events might arrive out of order."

DECISION: Last-write-wins based on event timestamp
- Compare incoming timestamp with stored last_seen
- Only update if incoming timestamp is newer
- Log out-of-order events for monitoring

WHY: Using timestamps (not arrival order) means the truth is in the event itself, 
not network timing.

PROBLEM IT SOLVES: If ping at T=100 arrives before ping at T=90, we don't let 
old data overwrite new data. Prevents false timeouts.


STEP 7: Deduplication
---------------------
"Clients retry on network failures. We might see duplicate events."

DECISION: Two-phase deduplication
1. Bloom filter: Fast probabilistic check (0.1% false positive)
2. Redis cache: Exact check with key "dedup:{job_id}:{timestamp}"

WHY: Bloom filter uses only 20MB for 10M jobs and catches 99.9% of duplicates 
instantly. Redis catches the 0.1% false positives.

PROBLEM IT SOLVES: Processing duplicate events wastes CPU and could cause 
incorrect state. This catches duplicates with minimal overhead.


STEP 8: The Core Challenge - Timeout Detection
-----------------------------------------------
"Now the hard part: detecting timeouts for millions of jobs efficiently."

DECISION: Timer Wheel (primary) + Periodic Sweep (backup)

Timer Wheel:
- Circular buffer with 3600 slots (1 per second)
- Each job goes in slot at (current_time + timeout) % 3600
- Every second, check the current slot

WHY: This is O(1) for insertion/deletion and O(jobs_in_slot) for checking. 
With uniform distribution, 1M jobs / 3600 slots = ~300 jobs per slot. We check 
300 jobs per second, not 1 million.

Alternative considered: Min-heap sorted by deadline
- Insertion: O(log N)
- Check: O(1) to peek, O(log N) to remove
- Problem: With 1M jobs, log(1M) = 20 operations per event. Timer wheel is O(1).

Alternative considered: Full scan every second
- O(N) to check all jobs
- Problem: Checking 1M jobs every second is 1M operations/sec just for scanning

PROBLEM IT SOLVES: We need sub-second timeout detection for millions of jobs. 
Timer wheel is the only structure that scales to this efficiently.

Periodic Sweep (backup):
- Every 60 seconds, scan Redis sorted set for overdue jobs
- Acts as safety net for bugs or crashes

WHY: Timer wheel is in-memory. If the timeout checker crashes, the wheel is 
lost. When it recovers, it rebuilds from Redis, but the sweep catches anything 
missed during the gap.

PROBLEM IT SOLVES: Provides fault tolerance. Even if timer wheel fails, we 
catch timeouts within 60 seconds instead of losing them entirely.


STEP 9: Partitioning for Scale
-------------------------------
"One server can't handle millions of jobs. We need horizontal scaling."

DECISION: Partition by job_id using consistent hashing
- Hash(job_id) % num_partitions
- Each partition has: event processor + timeout checker + Redis shard
- Typical: 100 partitions for 10M jobs

WHY: Partitioning gives independence. Each partition is a mini-system that 
doesn't coordinate with others. This means:
- Parallelism: 100 partitions = 100x throughput
- Isolation: Slow partition doesn't affect others
- Scalability: Add partitions to handle more load

PROBLEM IT SOLVES: Single server tops out around 100K jobs. Partitioning scales 
to 10M+ jobs by distributing work.


STEP 10: Fault Tolerance - Crash Recovery
------------------------------------------
"Servers crash. How do we ensure no timeouts are lost?"

DECISION: Multi-layer redundancy

Layer 1 - Kafka:
- Events stored durably with replication factor 3
- Can replay events after processor crash

Layer 2 - Redis:
- Active job state replicated to 2 replicas
- AOF (Append-Only File) for persistence

Layer 3 - Leader Election:
- Use ZooKeeper/etcd for timeout checker leadership
- One checker per partition, but standby ready to take over
- Failover in 5 seconds

WHY: Different failure modes need different solutions:
- Processor crash: Kafka replay
- Redis crash: Replica promotion
- Timeout checker crash: Leader election + rebuild from Redis

PROBLEM IT SOLVES: No single point of failure. If any component crashes, the 
system recovers automatically within seconds.


STEP 11: Query Performance
---------------------------
"Users need to query active jobs and historical timeouts."

DECISION: Different paths for different queries

Active jobs: GET /v1/jobs/active
- Query Redis sorted sets (by last_seen)
- Fan out to all partitions in parallel
- Merge results
- Latency: ~50ms

Historical timeouts: GET /v1/jobs/timeouts?since=24h_ago
- Query Postgres with indexed timestamp filter
- Table partitioned by day
- B-tree index on (status, last_seen)
- Latency: ~50ms

WHY: Redis excels at range queries with sorted sets. Postgres excels at complex 
queries with indexes. Use each for its strength.

PROBLEM IT SOLVES: Without partitioning Postgres by day, scanning 30 days of 
data would take seconds. Day partitions mean we only scan 1 day's partition.


STEP 12: Backpressure Handling
-------------------------------
"What if the system gets overloaded?"

DECISION: Reject requests early with 503
- When Kafka queue depth > 100K messages → return 503
- When Redis memory > 90% → return 503
- Clients implement exponential backoff

WHY: It's better to reject requests at the edge than to let them pile up and 
crash the system. Clients can retry later when load decreases.

PROBLEM IT SOLVES: Without backpressure, overload causes cascading failure. 
Queue fills up, latency spikes, timeouts, retries, more load, death spiral. 
Early rejection breaks the cycle.


STEP 13: Distributed Scheduler Integration
-------------------------------------------
"How does this integrate with the job scheduler?"

DECISION: WebSocket stream for timeout notifications
- Scheduler subscribes to /v1/stream/timeouts
- Real-time push when jobs timeout
- Scheduler triggers retry logic

WHY: Push is more efficient than polling. Scheduler gets notified instantly 
(sub-second) rather than polling every second.

PROBLEM IT SOLVES: With polling, there's a tradeoff: poll frequently (wasteful) 
or poll rarely (slow detection). WebSocket gives instant notifications with no 
polling overhead.


STEP 14: Retry Policy
----------------------
"When jobs timeout, should we retry?"

DECISION: Configurable exponential backoff
- max_retries: 3
- Delay: 5s → 10s → 20s (with jitter)
- New start event with same job_id, new attempt_id

WHY: Immediate retry on failure often fails again (worker still down). Exponential 
backoff gives the system time to recover. Jitter prevents thundering herd.

PROBLEM IT SOLVES: If all failed jobs retry simultaneously, they overwhelm the 
system. Jitter spreads retries over time.


STEP 15: Multi-Tenancy and Fairness
------------------------------------
"What if one tenant submits millions of jobs and starves others?"

DECISION: Per-tenant quotas
- Max 1,000 concurrent jobs per tenant
- Rate limit: 100 starts/minute per tenant
- Weighted fair queuing in scheduler

WHY: Without quotas, one misbehaving tenant can monopolize resources. Quotas 
provide isolation.

PROBLEM IT SOLVES: Noisy neighbor problem. Tenant A's load spike doesn't affect 
Tenant B's jobs.


STEP 16: Optimization - Local Caching
--------------------------------------
"Every event hits Redis. Can we reduce that?"

DECISION: LRU cache on each event processor
- Cache 100K recently accessed jobs
- Check cache first before Redis
- Hit rate: 70-80%

WHY: Popular jobs get many pings. Caching means we only hit Redis once, then 
serve subsequent pings from memory.

PROBLEM IT SOLVES: Reduces Redis load by 70-80%. This means we can handle more 
throughput with the same Redis infrastructure.


STEP 17: Edge Case - Jobs That Never End
-----------------------------------------
"What if a job never sends an end event? Memory leak?"

DECISION: Redis TTL = timeout + 2-minute buffer
- Automatically evicts from Redis after TTL
- Also removed from active sets when timed out

WHY: Even if buggy workers never send end events, jobs don't stay in memory 
forever. They timeout, get removed, and eventually evicted.

PROBLEM IT SOLVES: Prevents memory leaks from buggy clients. System is 
self-healing.


SUMMARY: The Full Flow
-----------------------
"Let me tie it all together with an example."

Job starts:
1. Worker sends: POST /v1/events {job_id: "abc", event_type: "start", 
   timeout: 300}
2. API publishes to Kafka partition hash("abc")
3. Event processor consumes, checks dedup, updates Redis + Postgres
4. Timer wheel inserts job into slot (now + 300) % 3600
5. Returns 202 to worker

Job pings:
1. Worker sends ping every 30 seconds
2. Same flow, but updates last_seen timestamp
3. Timer wheel moves job to new slot (now + 300) % 3600
4. Job never times out because pings keep resetting timer

Job times out:
1. Worker crashes, stops sending pings
2. 300 seconds later, timer wheel slot is checked
3. Job is in the slot, and now >= expiry_time
4. Mark as timed-out, remove from active sets, persist to Postgres
5. Publish timeout event to WebSocket
6. Scheduler receives event, triggers retry after 5s delay
7. New worker picks up job and starts over

Key Numbers:
- Throughput: 1M events/sec with 100 partitions
- Latency: <1ms ingestion, ~1s timeout detection
- Scale: 10M active jobs
- Fault tolerance: Recovery in 5-10 seconds


WHY THIS DESIGN WINS
---------------------
1. Scalability: Horizontal scaling via partitioning
2. Performance: Timer wheel + caching + batching
3. Fault tolerance: No single point of failure
4. Cost efficiency: Tiered storage (hot/cold)
5. Simplicity: Each partition is independent mini-system

The key insight: Don't solve everything at once. Partition the problem, solve 
it per-partition, then scale by adding partitions. This is how all large-scale 
distributed systems work.

"""