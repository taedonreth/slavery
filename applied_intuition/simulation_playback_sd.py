"""
================================================================================
12. INTERVIEW WALKTHROUGH SCRIPT (Start to Finish)
================================================================================

This is the narrative flow to present the design in an interview. Follow this 
structure to tell a coherent story.

STEP 1: Understand the Problem
-------------------------------
"Let me clarify the requirements. We're building a system to play back multi-GB 
simulation logs in a web browser with YouTube-like controls. Engineers need to 
scrub through logs, watch at different speeds, and see 3D visualizations of 
vehicles and pedestrians. The challenge is that logs can be 20-100 GB, contain 
millions of frames, and we need to support hundreds of concurrent users."

Key requirements:
- Stream massive log files (20-100 GB) efficiently
- Support random access for scrubbing (seek to any timestamp)
- 30-60 FPS smooth playback in browser
- Hundreds of concurrent users on same or different logs
- Sub-second seek latency


SYSTEM ARCHITECTURE DIAGRAM
---------------------------

┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT (Browser)                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌─────────────────────────────┐  │
│  │  UI Controls │    │  Frame Buffer│    │   Three.js Rendering        │  │
│  │  Play/Pause  │───▶│  (50 frames) │───▶│   InstancedMesh (Vehicles)  │  │
│  │  Seek/Scrub  │    │              │    │   InstancedMesh (Peds)      │  │
│  │  Speed       │    └──────────────┘    └─────────────────────────────┘  │
│  └──────────────┘                                                           │
│         │                     ▲                                             │
│         │ WebSocket          │ WebSocket                                    │
│         │ {action, frame}    │ {frame_data}                                 │
└─────────┼─────────────────────┼─────────────────────────────────────────────┘
          │                     │
          ▼                     │
┌─────────────────────────────────────────────────────────────────────────────┐
│                          APPLICATION SERVER                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐    │
│  │ WebSocket       │    │  Session Manager │    │ Prefetch Engine    │    │
│  │ Handler         │───▶│  (play state)    │───▶│ (next 1-2 chunks)  │    │
│  └─────────────────┘    └──────────────────┘    └────────────────────┘    │
│           │                      │                        │                 │
│           │                      ▼                        │                 │
│           │              ┌──────────────────┐             │                 │
│           └─────────────▶│  Frame Parser    │◀────────────┘                 │
│                          │  (chunk → frames)│                               │
│                          └──────────────────┘                               │
│                                   │                                          │
└───────────────────────────────────┼──────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           REDIS CACHE LAYER                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  Level 1: frame:log_id:frame_num  (TTL: 15 min)  [1-2ms latency]  │    │
│  │  Level 2: chunk:log_id:chunk_id   (TTL: 30 min)  [~10ms latency]  │    │
│  │  Level 3: metadata:log_id         (TTL: 60 min)  [~5ms latency]   │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                          Cache Hit ─┐      Cache Miss ─┐                    │
│                                     │                   │                    │
│                            (99% of requests)    (1% of requests)             │
│                                     │                   │                    │
└─────────────────────────────────────┼───────────────────┼──────────────────┘
                                      │                   │
                                      ▼                   ▼
                            ┌──────────────┐   ┌───────────────────┐
                            │ Return from  │   │   Download from   │
                            │    Cache     │   │    S3 Storage     │
                            └──────────────┘   └───────────────────┘
                                                         │
                                                         ▼
                                              ┌─────────────────────┐
                                              │  Chunk Structure:   │
                                              │  log_abc/           │
                                              │    ├─ chunk_0.bin   │
                                              │    ├─ chunk_1.bin   │
                                              │    ├─ chunk_N.bin   │
                                              │    └─ metadata.json │
                                              └─────────────────────┘


FLOW 1: OPENING A LOG
──────────────────────
User clicks log → GET /metadata → Return {frames, fps, duration} → Display timeline
                                   ▲
                                   └─ Redis cache (60 min TTL)


FLOW 2: PLAYING FROM START
───────────────────────────
1. User clicks Play
2. WebSocket: {action: "play", log_id: "ABC", frame: 0}
3. Check Redis for chunk_0
4. Cache MISS → Download chunk_0 from S3 (300ms)
5. Parse frame_0 → Send to client
6. Cache chunk_0 in Redis
7. Prefetch chunk_1 in background
8. Stream frames 1,2,3... from cached chunk_0 (1-2ms each)
9. Client buffers 50 frames → Smooth 30 FPS playback


FLOW 3: SEEKING (SCRUBBING)
────────────────────────────
1. User drags to 50% → frame 5000
2. Throttle: Only process every 100ms
3. Cancel in-flight requests
4. WebSocket: {action: "seek", frame: 5000}
5. Calculate: frame 5000 = chunk_5 (5000/1000)
6. Check Redis for chunk_5
7. Cache HIT → Parse frame 5000 (10ms)
   Cache MISS → Download chunk_5 from S3 (400ms)
8. Send frame 5000 to client
9. Prefetch chunks ±1 (chunk_4 and chunk_6)
10. User continues → smooth playback


FLOW 4: MULTI-USER SCENARIO
─────────────────────────────
User A (frame 100)  ─┐
User B (frame 5000) ─┼──▶ Redis Cache (Shared)
User C (frame 100)  ─┘
                      │
User A: Downloads chunk_0 → Caches it
User B: Downloads chunk_5 → Caches it
User C: Hits chunk_0 cache → Instant (<2ms) ✓


FLOW 5: COLLABORATIVE PLAYBACK
───────────────────────────────
┌──────────┐                ┌────────────────┐               ┌──────────┐
│ Leader   │───seek 1000───▶│  Redis PubSub  │──▶broadcast──▶│ Follower │
│ (User A) │                │ room:123:seek  │               │ (User B) │
└──────────┘                └────────────────┘               └──────────┘
                                    │
                                    ▼
                          All users jump to frame 1000


KEY PERFORMANCE METRICS
────────────────────────
• Cold start (first frame): ~500ms
• Cached seek: ~50ms  
• Frame delivery (cached): 1-2ms
• Chunk size: 1000 frames (~50 MB)
• Playback FPS: 30-60 FPS
• Buffer size: 50-100 frames
• Prefetch window: 150 frames ahead (playback) / 25 frames (scrubbing)
• Scale: Hundreds of concurrent users


STEP 2: Data Structure - Actor Representation
----------------------------------------------
"First, let me define what data we're visualizing. Each frame is a snapshot of 
the simulation world containing actors like vehicles, pedestrians, cyclists."

DECISION: Per-actor structure
{
  id: unique identifier
  type: ego | vehicle | pedestrian | cyclist
  position: [x, y, z] in world coordinates (meters)
  orientation: [x, y, z, w] quaternion
  dimensions: [length, width, height] in meters
  velocity: [vx, vy, vz] optional for debugging
}

WHY: 
- Position as world coordinates is straightforward and universal
- Quaternions (not Euler angles) because they avoid gimbal lock, interpolate 
  smoothly, and work efficiently with Three.js which uses them internally
- Dimensions define the bounding box for rendering

PROBLEM IT SOLVES: Euler angles suffer from gimbal lock and can't interpolate 
smoothly between frames. Quaternions are the standard for 3D rotation in games 
and simulations. At 200-400 bytes per actor, we can fit thousands in memory.


STEP 3: Reference Point Decision
---------------------------------
"Where is the [x, y, z] position measured from on each actor?"

DECISION: Use geometric center of bounding box as reference point
- Standardize across entire system
- All actors use the same convention

WHY: Geometric center is most intuitive for visualization and simplifies rotation 
math. If sensors are rear-axle mounted (common in vehicles), store the offset 
in metadata and transform in visualization layer, but never mix conventions.

PROBLEM IT SOLVES: If different actors use different reference points (one uses 
center, another uses rear axle), rotations place objects in wrong positions. 
This causes endless debugging nightmares. Standardization prevents this.


STEP 4: Frontend Challenge - Rendering Performance
---------------------------------------------------
"We need to render hundreds of bounding boxes at 30-60 FPS. How do we avoid 
crushing the browser?"

DECISION: Use Three.js InstancedMesh for batch rendering
- One InstancedMesh for all vehicles (up to 500 instances)
- One InstancedMesh for all pedestrians (up to 200)
- One InstancedMesh for cyclists (up to 100)
- Each mesh uses a transformation matrix per instance

WHY: If we create 500 individual box meshes, that's 500 separate GPU draw calls. 
The browser will drop frames. InstancedMesh does one draw call that renders 500 
copies of the same geometry. The GPU processes all instances in a single efficient 
pass.

PROBLEM IT SOLVES: With individual meshes at 500 actors, we get ~10 FPS (unusable). 
With InstancedMesh, we get 60 FPS easily. It's the difference between unusable 
and production-ready.

Alternative considered: Individual meshes per actor
- Simple to code, but 500 draw calls kills performance
- Browser stutters, frame rate drops to 10-15 FPS


STEP 5: Backend Challenge - Streaming Massive Files
----------------------------------------------------
"How do we stream a 20 GB log file efficiently?"

DECISION: Chunk the log into 1000-frame chunks (~50 MB each)
- Store in S3 or object storage
- Each chunk covers about 10 seconds at 100 FPS
- metadata.json describes total frames, FPS, chunk structure

WHY: Users don't watch the entire 20 GB log sequentially. They seek around. We 
need fast random access for scrubbing AND efficient sequential access for 
playback.

PROBLEM IT SOLVES: 
- If we stream the entire 20 GB: first frame takes forever, can't seek
- If chunks are too small (100 frames): too many HTTP requests, overhead adds up
- If chunks are too large (10,000 frames): slow seeks, download too much unused data
- 1000 frames is the sweet spot: ~50 MB per chunk, ~300ms download on good network

Alternative considered: Stream entire file
- Problem: 20 GB download before first frame shows (minutes of wait time)

Alternative considered: Frame-by-frame fetch
- Problem: 1 million frames = 1 million HTTP requests (completely impractical)


STEP 6: Seeking Implementation
-------------------------------
"User drags timeline to 50%, jumping from frame 0 to frame 5000. What happens?"

DECISION: Calculate chunk ID, fetch chunk, parse frame
- Frame 5000 is in chunk 5 (5000 / 1000 = 5)
- Download chunk 5 from S3 (~300-400ms)
- Parse frame 5000 from chunk
- Send to client
- Prefetch chunks 4 and 6 for scrubbing

WHY: We need to respond quickly to seeks. By knowing chunk boundaries, we can 
fetch exactly what we need. Prefetching adjacent chunks anticipates the user 
scrubbing nearby.

PROBLEM IT SOLVES: Without chunking, seeking to 50% means downloading 10 GB 
(half the file). With chunks, it's just 50 MB. That's 200x less data, which 
means sub-second seeks instead of minute-long waits.


STEP 7: Caching Strategy - Why Redis
-------------------------------------
"1000 users might watch the same popular log. Do we fetch from S3 every time?"

DECISION: Three-level Redis cache

Level 1 - Individual frames (15-min TTL):
- Key: "frame:{log_id}:{frame_num}"
- Serves repeat requests in 1-2ms instead of downloading chunk

Level 2 - Whole chunks (30-min TTL):
- Key: "chunk:{log_id}:{chunk_id}"
- Multiple frames from same chunk don't re-download

Level 3 - Metadata (1-hour TTL):
- Total frames, FPS, duration
- Rarely changes

WHY: S3 access is 300-500ms. Redis is 1-2ms. Popular logs (e.g., regression 
tests) get accessed repeatedly. First user downloads from S3, subsequent users 
hit cache.

PROBLEM IT SOLVES: Without caching, 1000 users on same log = 1000 S3 downloads. 
That's expensive ($$$) and slow. With caching, it's 1 S3 download + 999 cache 
hits. Fast and cheap.

Redis uses LRU eviction: when memory fills, oldest unused data evicts automatically. 
Hot data stays, cold data goes. Self-regulating.


STEP 8: Multi-User Independence
--------------------------------
"User A is at frame 0, User B at frame 5000, User C at frame 2000. How do we 
manage this?"

DECISION: Each user gets independent session in Redis
- Session key: "session:{session_id}"
- Contains: log_id, current_frame, playing (true/false)
- 30-minute TTL, refreshed on interaction

WHY: Users operate independently by default. They're debugging different issues 
in the same log. No coordination needed between sessions - each is isolated.

PROBLEM IT SOLVES: If we forced synchronized playback, only one user could control. 
That's terrible UX. Independent sessions mean 1000 users can watch the same log 
at different positions without interfering.


STEP 9: Playback Control - Play/Pause
--------------------------------------
"User clicks play. What's the flow?"

DECISION: WebSocket-based streaming
- Client sends: {action: "play", log_id: "abc", start_frame: 0}
- Server creates session, starts streaming frames
- Send frame, wait 33ms (for 30 FPS), send next frame, repeat
- Client buffers 50-100 frames locally

WHY: WebSocket provides full-duplex communication. Server can push frames 
continuously without client polling. Client maintains buffer to smooth over 
network jitter.

PROBLEM IT SOLVES: 
- Without buffer: Any network delay causes stuttering
- With 50-frame buffer: Can handle 1.5 seconds of delay smoothly
- HTTP polling would be inefficient (overhead on every request)


STEP 10: Prefetching Strategy
------------------------------
"How do we ensure smooth playback without stuttering?"

DECISION: Prefetch upcoming chunks
- During playback: prefetch 150 frames ahead (next 1-2 chunks)
- During scrubbing: prefetch only ±25 frames (smaller window)
- When scrubbing stops: expand to ±150 frames

WHY: Network is unpredictable. Prefetching loads data before it's needed. By 
the time user reaches frame 800, we've already fetched chunk 1 (frames 1000-1999).

PROBLEM IT SOLVES: Without prefetching, playback hits chunk boundary at frame 
1000 and has to wait 300ms for download. That's a visible stutter. With prefetching, 
the transition is seamless - data is ready before needed.


STEP 11: Adaptive Streaming
----------------------------
"Different users have different network speeds and device capabilities. How do 
we adapt?"

DECISION: Dynamic quality adjustment based on client feedback

Client reports every 2 seconds:
- Buffer length (how many frames queued)
- Render FPS (actual rate)
- Dropped frames
- Network latency

Server adjusts:
- If buffer overflowing (>150 frames): slow down sending
- If buffer starving (<30 frames): speed up sending
- If FPS drops (<30): reduce quality (send every other frame)
- If latency high (>200ms): increase prefetch window

WHY: One size doesn't fit all. Fast network + powerful device can handle high 
quality. Slow network or weak device needs reduced bandwidth and complexity.

PROBLEM IT SOLVES: Without adaptation, slow clients buffer forever (overload) 
or starve (stuttering). Adaptive streaming provides the best experience each 
client can handle.

Quality levels:
- High: Full 100 FPS, all actors, full precision
- Medium: 50 FPS (skip every other), actors within 100m, reduced precision
- Low: 25 FPS (every 4th frame), actors within 50m, maximum compression


STEP 12: Collaborative Playback
--------------------------------
"Multiple engineers want to watch the same log together in sync, like watching 
a movie. How?"

DECISION: Collaborative rooms with leader control
- User A creates room, becomes leader
- User B joins with room code
- Leader's actions (play/pause/seek) control everyone
- Redis PubSub for synchronization

Flow:
1. Leader seeks to frame 1000
2. Server publishes to Redis: "room:123:seek:1000"
3. All servers subscribed to room:123 receive message
4. Both User A and User B jump to frame 1000

WHY: Engineers debugging together need to see the same thing at the same time. 
"Look at what happens at 5 seconds!" only works if everyone sees it simultaneously.

PROBLEM IT SOLVES: Without sync, users constantly ask "what timestamp are you 
at?" and manually coordinate. With sync, leader drives and everyone follows 
automatically.

Each client still controls their own camera (orbit, zoom). View is independent, 
playback is synchronized.


STEP 13: Edge Case - Popular Logs
----------------------------------
"1000 users watch the same log. What happens to memory?"

DECISION: Shared Redis cache with LRU eviction
- First few users cause chunks to cache
- Subsequent users hit cache (no S3 download)
- Redis evicts least recently used data when full

WHY: Popular logs (regression tests, benchmark scenarios) get watched repeatedly. 
Instead of 1000 separate downloads, we leverage sharing.

PROBLEM IT SOLVES: 
- Memory efficient: Single log's hot chunks serve 1000 users
- If Redis fills up: LRU evicts cold data, keeps hot data
- System remains functional even under memory pressure


STEP 14: Edge Case - Rapid Scrubbing
-------------------------------------
"User rapidly drags timeline: frame 100 → 500 → 1200 → 800. Do we fetch all?"

DECISION: Throttle + cancel in-flight requests
- Only process seek every 100ms (ignore intermediate positions)
- Cancel previous request when new seek arrives
- Use smaller prefetch window (±25 frames) during scrubbing
- Expand window when scrubbing stops

WHY: During rapid scrubbing, user is exploring, not watching. They don't need 
every single frame - just responsive feedback. Most seek targets get abandoned 
before completing.

PROBLEM IT SOLVES: Without throttling, 100 seeks in 10 seconds = 100 chunk 
downloads (chaos). With throttling, it's maybe 5 downloads. Saves bandwidth 
and prevents overwhelming the server.


STEP 15: Edge Case - Network Interruption
------------------------------------------
"User's WiFi drops. What happens?"

DECISION: Graceful reconnection
- Frontend detects disconnect, shows "Reconnecting" indicator
- Attempt reconnection with exponential backoff
- On reconnect: send current state (session_id, last_frame)
- Server resumes from last position

WHY: Network issues are common. We need graceful degradation, not a blank screen.

PROBLEM IT SOLVES: Without reconnection logic, user has to refresh the page and 
start over. With automatic reconnection, disruption is minimal - playback resumes 
where it left off.


STEP 16: Edge Case - Very Large Logs (100 GB)
----------------------------------------------
"Standard chunking might not be enough for 100 GB logs. What else?"

DECISION: Hierarchical chunking + progressive loading

Hierarchical chunking:
- Level 1: 1000-frame chunks (full data)
- Level 2: 10,000-frame superchunks (ego vehicle only for overview)

Progressive loading:
- Load ego vehicle first (1-2 actors) → user sees something immediately
- Stream other actors in subsequent passes → details fill in

Thumbnail timeline:
- Pre-generate keyframes every 100th frame (reduced quality)
- Show thumbnails on timeline for scrubbing preview

WHY: Users need context quickly. Showing ego vehicle in 200ms is better than 
waiting 2 seconds for everything.

PROBLEM IT SOLVES: With 100 GB logs, even 50 MB chunks feel slow. Progressive 
loading provides instant feedback while full details load in background.


STEP 17: Optimization - Why Client-Side Rendering
--------------------------------------------------
"Should we render on server and stream video, or render in browser?"

DECISION: Client-side rendering (our choice)
- Server sends raw data (positions, quaternions)
- Browser renders 3D scene with Three.js
- Each user controls their own camera

WHY: 
- Server is stateless and scales easily
- Users get interactive camera control (rotate, zoom, pan freely)
- Network bandwidth is lower (data is smaller than video)
- Users with powerful devices get higher quality

Alternative considered: Server-side rendering (video stream)
- Advantages: Works on any device, consistent quality
- Disadvantages: Loses camera interactivity, requires massive GPU infrastructure, 
  higher bandwidth

PROBLEM IT SOLVES: Engineers need to inspect scenes from different angles. 
Server-side rendering means every view change requires server round trip. Client-side 
rendering gives instant camera control.


SUMMARY: The Complete Flow
---------------------------
"Let me show you the end-to-end flow."

Opening a log:
1. User clicks log "ABC123"
2. Frontend: GET /api/logs/ABC123/metadata
3. Backend: Return {total_frames: 10000, fps: 100, duration: "100s"}
4. Frontend: Display timeline

Playing:
1. User clicks play
2. Frontend: WebSocket connect, send {action: "play", log_id: "ABC123", frame: 0}
3. Backend: Create session, check Redis for chunk 0
4. Cache miss → download chunk 0 from S3 (300ms)
5. Parse frame 0, send to client
6. Background: Cache chunk 0, parse frames 1-999, prefetch chunk 1
7. Frontend: Render frame 0 with InstancedMesh, buffer frames
8. Backend: Stream frames 1, 2, 3... at 30 FPS
9. All frames from cached chunk 0 now (1-2ms each)
10. Client buffer grows to 50 frames → smooth playback

Seeking:
1. User drags to 50% (frame 5000)
2. Frontend: Throttle, send {action: "seek", frame: 5000}, clear buffer
3. Backend: Calculate chunk 5, check Redis
4. Cache miss → download chunk 5 from S3 (400ms)
5. Parse frame 5000, send to client, cache chunk 5
6. Prefetch chunks 4 and 6 bidirectionally
7. Frontend: Render frame 5000, ready for continued playback

Multiple users:
- User A at frames 0-100: Uses chunk 0 (cached)
- User B at frames 5000-5100: Uses chunk 5 (cached)
- User C seeks to frame 100: Hits chunk 0 cache (instant, <10ms)
- Memory efficient: Only 2 chunks cached (100 MB) for 3 users


Key Numbers:
-------------
- Chunk size: 1000 frames (~50 MB)
- Cache TTLs: 15 min (frames), 30 min (chunks), 60 min (metadata)
- Latency: ~500ms cold start, ~50ms cached seeks, 1-2ms frame delivery
- Scale: Hundreds of concurrent users
- Frame rate: 30-60 FPS playback


WHY THIS DESIGN WINS
---------------------
1. **Random Access**: Chunking enables fast seeks to any timestamp
2. **Smooth Playback**: Prefetching + buffering prevents stuttering
3. **Scalability**: Shared caching means users benefit from each other
4. **Performance**: InstancedMesh renders 500 actors in one draw call
5. **Adaptability**: Quality adjusts to network/device capabilities
6. **Cost-Efficient**: Popular logs cached, cold logs fetched on-demand

The key insight: Treat log playback like video streaming. Chunk the data, cache 
hot content, prefetch intelligently, and adapt to client capabilities. This is 
how YouTube streams 4K video to millions - we apply the same principles to 
simulation logs.


ALTERNATIVE APPROACHES & TRADEOFFS
-----------------------------------

Alternative 1: Delta Encoding (store only changes between frames)
- Pro: Smaller file size
- Con: Can't seek randomly (need to replay from start to build state)
- Our choice: Frame-based storage trades size for random access

Alternative 2: Server-Side Rendering (send video stream)
- Pro: Works on any device
- Con: No camera control, expensive GPU servers, higher bandwidth
- Our choice: Client-side rendering for interactivity

Alternative 3: Smaller chunks (100 frames)
- Pro: Lower latency per chunk
- Con: Too many HTTP requests, overhead adds up
- Our choice: 1000 frames balances latency with efficiency

Alternative 4: Larger chunks (10,000 frames)
- Pro: Fewer HTTP requests
- Con: Slow seeks, download too much unused data
- Our choice: 1000 frames provides fast seeks

Alternative 5: Database storage (frames in PostgreSQL)
- Pro: Standard query interface
- Con: Databases aren't designed for large binary blobs, slow
- Our choice: Object storage (S3) is cheap and fast for blobs


COMMON FOLLOW-UP QUESTIONS
---------------------------

Q: "How do you handle different coordinate systems across logs?"
A: Standardize on one system (e.g., right-handed Z-up) and transform at ingest 
   time. Store transform metadata with log.

Q: "What if two users scrub to the same frame at the same instant?"
A: Both hit the same Redis cache. Frame cache is shared, so second user gets 
   instant response.

Q: "How much does Redis caching really save?"
A: For popular logs: First user = 300ms (S3), next 999 users = 1-2ms (Redis). 
   That's 150-300x faster.

Q: "What happens if S3 is slow or down?"
A: Requests timeout after 5 seconds. Show error to user with retry button. 
   Redis cache keeps serving recently accessed data.

Q: "Why Three.js specifically?"
A: It's the most popular WebGL library with excellent performance, active 
   community, and built-in quaternion support. Alternatives like Babylon.js 
   would work too.

Q: "Could you use WebRTC instead of WebSocket?"
A: WebRTC is for peer-to-peer media streaming. WebSocket is simpler for 
   server-client data streaming. WebRTC would add complexity without benefits.

"""