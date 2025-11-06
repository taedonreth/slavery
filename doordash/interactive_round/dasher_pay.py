from datetime import datetime
from typing import List, Dict, Tuple, Optional
from collections import defaultdict


class DasherPaymentCalculator:
    """
    Calculates dasher payments based on delivery events.
    Supports multiple payment models and peak hour pricing.
    """

    def __init__(self, base_rate: float = 0.3):
        self.base_rate = base_rate

    def parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse timestamp string to datetime object."""
        # Support multiple formats
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%H:%M",
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(timestamp_str, fmt)
                # If only time provided, use a default date
                if fmt == "%H:%M":
                    dt = dt.replace(year=2025, month=1, day=1)
                return dt
            except ValueError:
                continue
        raise ValueError(f"Unable to parse timestamp: {timestamp_str}")

    def calculate_minutes(self, start: datetime, end: datetime) -> float:
        """Calculate minutes between two timestamps."""
        return (end - start).total_seconds() / 60

    def calculate_payment_part1(self, events: List[Dict]) -> float:
        """
        Part 1: Basic payment calculation.
        Pay = base_rate * minutes * number_of_concurrent_orders
        """
        # Sort events by timestamp
        sorted_events = sorted(
            events, key=lambda x: self.parse_timestamp(x["timestamp"])
        )

        total_pay = 0.0
        active_orders = set()
        prev_time = None

        for event in sorted_events:
            curr_time = self.parse_timestamp(event["timestamp"])

            # Calculate payment for the time interval
            if prev_time and active_orders:
                minutes = self.calculate_minutes(prev_time, curr_time)
                num_orders = len(active_orders)
                pay = num_orders * self.base_rate * minutes
                total_pay += pay

            # Update active orders
            if event["status"] == "ACCEPTED":
                active_orders.add(event["deliveryId"])
            elif event["status"] in ["DELIVERED", "FULFILLED"]:
                active_orders.discard(event["deliveryId"])

            prev_time = curr_time

        return round(total_pay, 2)

    def calculate_payment_part2(self, events: List[Dict]) -> float:
        """
        Part 2: Adjusted payment - wait time at pickup location doesn't count for other orders.
        When dasher is at a pickup location (ARRIVED to PICKED_UP), only that order gets credit.
        """
        sorted_events = sorted(
            events, key=lambda x: self.parse_timestamp(x["timestamp"])
        )

        total_pay = 0.0
        active_orders = set()
        at_pickup = {}  # deliveryId -> True if currently at pickup location
        prev_time = None

        for event in sorted_events:
            curr_time = self.parse_timestamp(event["timestamp"])

            # Calculate payment for the time interval
            if prev_time and active_orders:
                minutes = self.calculate_minutes(prev_time, curr_time)

                # Count orders that should get credit
                orders_at_pickup = [oid for oid in at_pickup if at_pickup[oid]]

                if orders_at_pickup:
                    # Only the order at pickup gets credit
                    pay = self.base_rate * minutes
                else:
                    # All active orders get credit
                    num_orders = len(active_orders)
                    pay = num_orders * self.base_rate * minutes

                total_pay += pay

            # Update state based on event
            delivery_id = event["deliveryId"]
            status = event["status"]

            if status == "ACCEPTED":
                active_orders.add(delivery_id)
                at_pickup[delivery_id] = False
            elif status == "ARRIVED":
                at_pickup[delivery_id] = True
            elif status == "PICKED_UP":
                at_pickup[delivery_id] = False
            elif status in ["DELIVERED", "FULFILLED"]:
                active_orders.discard(delivery_id)
                at_pickup.pop(delivery_id, None)

            prev_time = curr_time

        return round(total_pay, 2)

    def calculate_payment_part3(
        self, events: List[Dict], peak_windows: List[List[str]]
    ) -> float:
        """
        Part 3: Peak hour pricing - double pay during specified time windows.
        """
        sorted_events = sorted(
            events, key=lambda x: self.parse_timestamp(x["timestamp"])
        )

        # Parse peak windows
        peak_periods = []
        for window in peak_windows:
            start = self.parse_timestamp(window[0])
            end = self.parse_timestamp(window[1])
            peak_periods.append((start, end))

        total_pay = 0.0
        active_orders = set()
        at_pickup = {}
        prev_time = None

        for event in sorted_events:
            curr_time = self.parse_timestamp(event["timestamp"])

            # Calculate payment for the time interval
            if prev_time and active_orders:
                # Split interval by peak/non-peak periods
                pay = self._calculate_interval_pay(
                    prev_time, curr_time, active_orders, at_pickup, peak_periods
                )
                total_pay += pay

            # Update state
            delivery_id = event["deliveryId"]
            status = event["status"]

            if status == "ACCEPTED":
                active_orders.add(delivery_id)
                at_pickup[delivery_id] = False
            elif status == "ARRIVED":
                at_pickup[delivery_id] = True
            elif status == "PICKED_UP":
                at_pickup[delivery_id] = False
            elif status in ["DELIVERED", "FULFILLED"]:
                active_orders.discard(delivery_id)
                at_pickup.pop(delivery_id, None)

            prev_time = curr_time

        return round(total_pay, 1)

    def _calculate_interval_pay(
        self,
        start: datetime,
        end: datetime,
        active_orders: set,
        at_pickup: dict,
        peak_periods: List[Tuple[datetime, datetime]],
    ) -> float:
        """Calculate pay for an interval, splitting by peak/non-peak periods."""
        # Create timeline points
        points = [start, end]
        for peak_start, peak_end in peak_periods:
            if start < peak_start < end:
                points.append(peak_start)
            if start < peak_end < end:
                points.append(peak_end)

        points = sorted(set(points))
        total_pay = 0.0

        # Calculate pay for each sub-interval
        for i in range(len(points) - 1):
            interval_start = points[i]
            interval_end = points[i + 1]
            minutes = self.calculate_minutes(interval_start, interval_end)

            # Determine if in peak period
            is_peak = any(
                peak_start <= interval_start < peak_end
                for peak_start, peak_end in peak_periods
            )

            rate = self.base_rate * 2 if is_peak else self.base_rate

            # Count orders that should get credit
            orders_at_pickup = [oid for oid in at_pickup if at_pickup.get(oid, False)]

            if orders_at_pickup:
                pay = rate * minutes
            else:
                num_orders = len(active_orders)
                pay = num_orders * rate * minutes

            total_pay += pay

        return total_pay


class DasherPaymentAPI:
    """
    API wrapper for dasher payment calculations.
    Simulates calling a downstream service for delivery data.
    """

    def __init__(self):
        self.calculator = DasherPaymentCalculator(base_rate=0.3)
        # Simulated database/downstream service
        self.delivery_service = DeliveryService()

    def calculate_reward(
        self,
        dasher_id: int,
        peak_windows: Optional[List[List[str]]] = None,
        use_part2_logic: bool = False,
    ) -> Dict:
        """
        Main API endpoint to calculate dasher reward.

        Args:
            dasher_id: ID of the dasher
            peak_windows: Optional list of peak hour windows
            use_part2_logic: Whether to use Part 2 logic (pickup wait time)

        Returns:
            Dictionary with dasher_id and total_reward
        """
        try:
            # Call downstream service to get delivery events
            events = self.delivery_service.get_deliveries(dasher_id)

            if not events:
                return {
                    "dasher_id": dasher_id,
                    "total_reward": 0.0,
                    "message": "No deliveries found",
                }

            # Calculate payment based on logic version
            if peak_windows:
                if use_part2_logic:
                    total_pay = self.calculator.calculate_payment_part3(
                        events, peak_windows
                    )
                else:
                    # For simplicity, Part 3 includes Part 2 logic
                    total_pay = self.calculator.calculate_payment_part3(
                        events, peak_windows
                    )
            elif use_part2_logic:
                total_pay = self.calculator.calculate_payment_part2(events)
            else:
                total_pay = self.calculator.calculate_payment_part1(events)

            return {
                "dasher_id": dasher_id,
                "total_reward": total_pay,
                "num_deliveries": len(
                    set(e["deliveryId"] for e in events if e["status"] == "ACCEPTED")
                ),
            }

        except Exception as e:
            return {"dasher_id": dasher_id, "error": str(e), "total_reward": 0.0}

    def calculate_rewards_bulk(self, dasher_ids: List[int], **kwargs) -> List[Dict]:
        """Calculate rewards for multiple dashers."""
        return [self.calculate_reward(dasher_id, **kwargs) for dasher_id in dasher_ids]


class DeliveryService:
    """Simulates a downstream service that provides delivery data."""

    def __init__(self):
        # Sample data
        self.data = [
            {
                "dasherId": 1,
                "deliveryId": 1,
                "timestamp": "06:15",
                "status": "ACCEPTED",
            },
            {
                "dasherId": 1,
                "deliveryId": 2,
                "timestamp": "06:18",
                "status": "ACCEPTED",
            },
            {"dasherId": 1, "deliveryId": 1, "timestamp": "06:19", "status": "ARRIVED"},
            {
                "dasherId": 1,
                "deliveryId": 1,
                "timestamp": "06:22",
                "status": "PICKED_UP",
            },
            {"dasherId": 1, "deliveryId": 2, "timestamp": "06:30", "status": "ARRIVED"},
            {
                "dasherId": 1,
                "deliveryId": 2,
                "timestamp": "06:33",
                "status": "PICKED_UP",
            },
            {
                "dasherId": 1,
                "deliveryId": 1,
                "timestamp": "06:36",
                "status": "DELIVERED",
            },
            {
                "dasherId": 1,
                "deliveryId": 2,
                "timestamp": "06:45",
                "status": "DELIVERED",
            },
        ]

    def get_deliveries(self, dasher_id: int) -> List[Dict]:
        """Retrieve all delivery events for a specific dasher."""
        return [event for event in self.data if event["dasherId"] == dasher_id]


# Demo usage
if __name__ == "__main__":
    api = DasherPaymentAPI()

    print("=== Part 1: Basic Payment ===")
    result = api.calculate_reward(dasher_id=1, use_part2_logic=False)
    print(f"Dasher {result['dasher_id']} reward: ${result['total_reward']}")

    print("\n=== Part 2: Adjusted Payment (Pickup Wait Time) ===")
