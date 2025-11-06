import random
from threading import Lock


# ---------------------------
# User / Dasher definitions
# ---------------------------
class User:
    def __init__(self, user_id):
        self.id = user_id


class Dasher(User):
    pass


# ---------------------------
# Delivery Assignment Service
# ---------------------------
class DeliveryAssignmentService:
    def __init__(self):
        # Original bug: map not initialized
        self.dasher_map = {}  # key: consecutive index, value: Dasher
        self.lock = Lock()  # for thread safety

    def addDasher(self, dasher: Dasher):
        """Add a new available dasher"""
        with self.lock:
            # Use current size as next index
            index = len(self.dasher_map)
            self.dasher_map[index] = dasher
            # NOTE: remote recording should be done asynchronously
            # remote_record_service(dasher, "added")

    def pickDasher(self):
        """Randomly pick a dasher and maintain consecutive keys"""
        with self.lock:
            size = len(self.dasher_map)
            if size == 0:
                return None

            # Random key in current range
            key = random.randint(0, size - 1)
            dasher = self.dasher_map[key]

            # Adjust map to remove gaps
            if key != size - 1:
                # Move last dasher into removed slot
                self.dasher_map[key] = self.dasher_map[size - 1]

            # Remove the last key
            del self.dasher_map[size - 1]

            # NOTE: remote recording should be async
            # remote_record_service(dasher, "picked")

            return dasher


# ---------------------------
# Example usage
# ---------------------------
if __name__ == "__main__":
    service = DeliveryAssignmentService()

    # Add 5 dashers
    for i in range(5):
        service.addDasher(Dasher(i))

    # Pick 3 dashers randomly
    for _ in range(3):
        d = service.pickDasher()
        print(f"Picked dasher id: {d.id}")

    # Remaining dashers
    print("Remaining dashers in map:", [d.id for d in service.dasher_map.values()])
