class DeliveryStatus(Enum):
    ACCEPTED = "ACCEPTED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


@dataclass
class DeliveryRecord:
    dasherId: int
    deliveryId: int
    timestamp: str
    status: str


class DeliveryRewardAPI:
    """
    API endpoint that calculates dasher rewards based on delivery history.
    
    Reward Formula:
    - Successful delivery (ACCEPTED -> DELIVERED): $10
    - Cancelled delivery (ACCEPTED -> CANCELLED): $0
    - Rush hour bonus (5 PM - 9 PM): 2x multiplier
    """
    
    def __init__(self, base_reward: float = 10.0, rush_hour_multiplier: float = 2.0):
        self.base_reward = base_reward
        self.rush_hour_multiplier = rush_hour_multiplier
        self.rush_hour_start = 17  # 5 PM
        self.rush_hour_end = 21    # 9 PM
    
    def is_rush_hour(self, timestamp_str: str) -> bool:
        """Check if timestamp falls within rush hour window (5 PM - 9 PM)."""
        try:
            dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            return self.rush_hour_start <= dt.hour < self.rush_hour_end
        except ValueError:
            raise ValueError(f"Invalid timestamp format: {timestamp_str}")
    
    def calculate_reward(self, dasher_id: int, delivery_records: List[Dict]) -> float:
        """
        Calculate total reward for a dasher based on their delivery records.
        
        Args:
            dasher_id: The dasher's unique identifier
            delivery_records: List of delivery records with status updates
            
        Returns:
            Total reward amount
        """
        # Filter records for this dasher
        dasher_records = [r for r in delivery_records if r['dasherId'] == dasher_id]
        
        # Group by deliveryId using defaultdict
        deliveries = defaultdict(list)
        for record in dasher_records:
            deliveries[record['deliveryId']].append(record)
        
        total_reward = 0.0
        
        # Process each delivery
        for delivery_id, records in deliveries.items():
            # Sort by timestamp to get correct sequence
            records.sort(key=lambda x: x['timestamp'])
            
            # Validate: should have ACCEPTED first
            if len(records) < 2 or records[0]['status'] != 'ACCEPTED':
                continue
            
            final_status = records[-1]['status']
            
            # Only reward completed deliveries
            if final_status == 'DELIVERED':
                delivery_timestamp = records[-1]['timestamp']
                reward = self.base_reward
                
                # Apply rush hour multiplier
                if self.is_rush_hour(delivery_timestamp):
                    reward *= self.rush_hour_multiplier
                
                total_reward += reward
        
        return total_reward
