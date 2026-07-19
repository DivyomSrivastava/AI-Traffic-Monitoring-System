class LineCounter:
    """
    Counts vehicles only when they cross the virtual counting line.
    """

    def __init__(self, line_y):

        # Y-coordinate of counting line
        self.line_y = line_y

        # Previous center position of every tracked vehicle
        self.previous_positions = {}

        # IDs already counted
        self.counted_ids = set()

        # Vehicle counts
        self.total_count = 0

        self.car_count = 0
        self.motorcycle_count = 0
        self.bus_count = 0
        self.truck_count = 0

    def update(self, track_id, class_id, center_y):
        """
        Updates vehicle position and checks if it crossed the line.

        Parameters
        ----------
        track_id : int
            ByteTrack ID

        class_id : int
            COCO Class ID

        center_y : int
            Current center Y coordinate
        """

        # First appearance of vehicle
        if track_id not in self.previous_positions:
            self.previous_positions[track_id] = center_y
            return

        previous_y = self.previous_positions[track_id]

        # Update latest position
        self.previous_positions[track_id] = center_y

        # Ignore already counted vehicles
        if track_id in self.counted_ids:
            return

        # Vehicle crossed line from top to bottom
        if previous_y < self.line_y and center_y >= self.line_y:

            self.counted_ids.add(track_id)

            self.total_count += 1

            if class_id == 2:
                self.car_count += 1

            elif class_id == 3:
                self.motorcycle_count += 1

            elif class_id == 5:
                self.bus_count += 1

            elif class_id == 7:
                self.truck_count += 1

    def get_counts(self):

        return {
            "Cars": self.car_count,
            "Motorcycles": self.motorcycle_count,
            "Buses": self.bus_count,
            "Trucks": self.truck_count,
            "Total": self.total_count
        }