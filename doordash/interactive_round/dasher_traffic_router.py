"""
*Prompt: You are a Backend Engineer at DoorDash and realized that your service can no longer keep up with traffic. In order to deal with the increased load, your team has decided to scale horizontally by adding more pods that run your service. In order to achieve this, your colleague implemented a traffic router that distributes incoming traffic among pods using a round robin algorithm (requests are routed to pods on a cyclical basis). Unfortunately, their implementation doesn't quite seem to work and you are tasked with debugging the code. Their implementation consists of the following classes: • TrafficRouter: Represents the Traffic Router. Its constructor takes a list of Backend pods as an argument. • Pod: Represents a Pod running your service application. Its constructor takes hostname and port as arguments. • Backend: Represents a Pod and its state ("AVAILABLE", "UNAVAILABLE"). Its constructor takes a Pod and a state as arguments. • HttpRequest: Represents an incoming Http Request. Its constructor takes an id as an argument. All requests from a user share the same request id. And the following methods: • TrafficRouter.getBackend(request: HttpRequest): Returns the next available Pod that can serve the request using a round robin heuristic. If all Pods are unavailable, returns null. • TrafficRouter.reportAvailability(backen d: Backend, state: State): Marks a Backend Pod as either available or unavailable. • TrafficRouter.addBackend(backend: Backend): Adds new backends to the rotation at runtime.H
"""

from enum import Enum


class State(Enum):
    AVAILABLE = 1
    UNAVAILABLE = 2


class Pod:
    def __init__(self, hostname: str):
        self.hostname = hostname

    def __repr__(self):
        return f"Pod({self.hostname})"


class Backend:
    def __init__(self, pod: Pod, state: State):
        self.pod = pod
        self.state = state

    def __repr__(self):
        return f"Backend({self.pod}, {self.state.name})"


class HttpRequest:
    def __init__(self, request_id: str):
        self.id = request_id


class TrafficRouter:
    def __init__(self, backends: list[Backend]):
        self.backends = backends
        # Bug Fix: Use an instance variable for the index, not a local one
        self.current_index = 0
        self.lock = threading.Lock()  # Added for thread-safety

    def get_backend(self, request: HttpRequest) -> Pod | None:
        with self.lock:
            # Bug Fix: Must check for empty backend list
            if not self.backends:
                return None

            num_backends = len(self.backends)

            # Bug Fix: Loop up to num_backends times to check every pod
            for _ in range(num_backends):
                # Get the pod at the current round-robin index
                backend = self.backends[self.current_index]

                # Advance the index for the *next* call
                # Use modulo to wrap around to 0
                self.current_index = (self.current_index + 1) % num_backends

                # Bug Fix: Check against the correct "AVAILABLE" state
                if backend.state == State.AVAILABLE:
                    return backend.pod  # Found one, return it

            # Bug Fix: If we looped through all pods and found none, return None
            return None

    def add_backend(self, backend: Backend):
        with self.lock:
            # This logic must be careful not to mess up the current_index
            # if it's running live. Simplest way is to append.
            self.backends.append(backend)

    def report_availability(self, pod_hostname: str, state: State):
        with self.lock:
            for backend in self.backends:
                if backend.pod.hostname == pod_hostname:
                    backend.state = state
                    print(f"Updated {pod_hostname} to {state.name}")
                    break


# --- Demonstration ---
p1 = Backend(Pod("server1"), State.AVAILABLE)
p2 = Backend(Pod("server2"), State.UNAVAILABLE)
p3 = Backend(Pod("server3"), State.AVAILABLE)

router = TrafficRouter([p1, p2, p3])

print(f"Request 1 -> {router.get_backend(HttpRequest('a'))}")  # server1
print(f"Request 2 -> {router.get_backend(HttpRequest('b'))}")  # server3 (skips server2)
print(f"Request 3 -> {router.get_backend(HttpRequest('c'))}")  # server1 (wraps around)

print("\n--- Marking server1 as UNAVAILABLE ---")
router.report_availability("server1", State.UNAVAILABLE)

print(f"Request 4 -> {router.get_backend(HttpRequest('d'))}")  # server3
print(f"Request 5 -> {router.get_backend(HttpRequest('e'))}")  # server3 (skips 1 and 2)

print("\n--- Marking all as UNAVAILABLE ---")
router.report_availability("server3", State.UNAVAILABLE)

print(f"Request 6 -> {router.get_backend(HttpRequest('f'))}")  # None
