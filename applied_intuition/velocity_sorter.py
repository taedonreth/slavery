
"""
Given a json log containing the velocities of many vehicles at different timestamps, find the 
fastest vehicle and the largest velocity range. Follow up questions asked how to find the avg 
velocity within 5 seconds and how to filter out outliers (velocity that is too large).
"""

class VehicleAnalytics:
    """
    Analyzes vehicle velocity logs using custom-written binary search for
    efficient time-window queries.
    """
    def __init__(self, log_data):
        if not log_data:
            raise ValueError("Log data cannot be empty.")
        self.log_data = log_data
        self.vehicle_stats = {}
        self._process_logs()

    def _process_logs(self):
        for record in self.log_data:
            velocity = record['velocity']
            v_id = record['vehicle_id']
            timestamp = record['timestamp']
            if v_id not in self.vehicle_stats:
                self.vehicle_stats[v_id] = {'min_v': velocity, 'max_v': velocity, 'readings': []}
            stats = self.vehicle_stats[v_id]
            stats['min_v'] = min(stats['min_v'], velocity)
            stats['max_v'] = max(stats['max_v'], velocity)
            stats['readings'].append((timestamp, velocity))
        for v_id in self.vehicle_stats:
            self.vehicle_stats[v_id]['readings'].sort()

    def _find_left_boundary(self, timestamps, target_time):
        """
        Finds the index of the first element >= target_time using an inclusive-high search.
        """
        low, high = 0, len(timestamps) - 1
        result_index = len(timestamps)  # Default to insertion point at the end

        while low <= high:
            mid = low + (high - low) // 2
            if timestamps[mid] >= target_time:
                result_index = mid  # Found a potential candidate
                high = mid - 1      # Look for an even earlier one on the left
            else:
                low = mid + 1       # Candidate must be on the right
        return result_index

    def _find_right_boundary(self, timestamps, target_time):
        """
        Finds the index of the first element > target_time using an inclusive-high search.
        """
        low, high = 0, len(timestamps) - 1
        result_index = len(timestamps)  # Default to insertion point at the end

        while low <= high:
            mid = low + (high - low) // 2
            if timestamps[mid] > target_time:
                result_index = mid  # Found a potential candidate
                high = mid - 1      # Look for an even earlier one on the left
            else:
                low = mid + 1       # Candidate must be on the right
        return result_index

    def get_avg_velocity_in_window(self, vehicle_id, start_time, end_time):
        """
        Calculates average velocity within a time window using custom binary search.
        """
        if vehicle_id not in self.vehicle_stats:
            print(f"Warning: Vehicle ID '{vehicle_id}' not found.")
            return 0.0

        readings = self.vehicle_stats[vehicle_id]['readings']
        if not readings:
            return 0.0

        timestamps = [r[0] for r in readings]

        # Use our custom binary search functions to find the window
        start_index = self._find_left_boundary(timestamps, start_time)
        end_index = self._find_right_boundary(timestamps, end_time)

        readings_in_window = readings[start_index:end_index]

        if not readings_in_window:
            return 0.0

        total_velocity = sum(reading[1] for reading in readings_in_window)
        return total_velocity / len(readings_in_window)

    def get_fastest_vehicle(self):
        if not self.vehicle_stats:
            return (None, -1)
        
        fastest_id = None
        max_velocity = -1
        
        for v_id, stats in self.vehicle_stats.items():
            if stats['max_v'] > max_velocity:
                max_velocity = stats['max_v']
                fastest_id = v_id
        
        return (fastest_id, max_velocity)

    def get_vehicle_with_largest_range(self):
        if not self.vehicle_stats:
            return (None, -1)
        
        largest_range_id = None
        largest_range = -1
        
        for v_id, stats in self.vehicle_stats.items():
            velocity_range = stats['max_v'] - stats['min_v']
            if velocity_range > largest_range:
                largest_range = velocity_range
                largest_range_id = v_id
        
        return (largest_range_id, largest_range)

"""
def _calculate_percentile(sorted_data, percentile):
    '''
    Calculates the value at a given percentile for a sorted list of data
    using linear interpolation. Does not use any external modules.
    '''
    if not sorted_data:
        return 0
    n = len(sorted_data)
    if n == 1:
        return sorted_data[0]
        
    # Calculate the ordinal rank.
    rank = (percentile / 100) * (n - 1)
    
    lower_index = int(rank)
    
    # If rank is an integer, it's a direct value
    if lower_index == rank:
        return sorted_data[lower_index]
    
    # For interpolation, get the fractional part
    fraction = rank - lower_index
    
    upper_index = lower_index + 1
    # Ensure upper_index is within bounds
    if upper_index >= n:
        return sorted_data[lower_index]

    lower_value = sorted_data[lower_index]
    upper_value = sorted_data[upper_index]
    
    # Linearly interpolate between the two values
    return lower_value + (upper_value - lower_value) * fraction

def filter_velocity_outliers(log_data):
    '''
    Filters out log entries with outlier velocities using the IQR method.
    This version does not use any external modules for its calculations.

    An outlier is defined as any velocity greater than Q3 + 1.5 * IQR.

    Args:
        log_data (list): The raw list of log entry dictionaries.

    Returns:
        A new list of log entries with outliers removed.
    '''
    if not log_data:
        return []

    # 1. Collect all velocities to determine the distribution
    all_velocities = [record['velocity'] for record in log_data]
    
    # Sort the data, which is required for percentile calculation
    all_velocities.sort()

    # 2. Calculate the first quartile (Q1) and third quartile (Q3) manually
    q1 = _calculate_percentile(all_velocities, 25)
    q3 = _calculate_percentile(all_velocities, 75)
    
    # 3. Compute the Interquartile Range (IQR)
    iqr = q3 - q1
    
    # 4. Establish the upper bound for non-outlier data
    upper_bound = q3 + 1.5 * iqr
    print(f"Calculated outlier threshold. Any velocity > {upper_bound:.2f} will be removed.")
    
    # 5. Create a new list containing only the entries within the valid range
    filtered_logs = [record for record in log_data if record['velocity'] <= upper_bound]
    
    return filtered_logs
"""