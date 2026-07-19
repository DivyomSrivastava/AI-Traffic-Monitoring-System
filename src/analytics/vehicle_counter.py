class VehicleCounter:

    def __init__(self):

        # Stores IDs that have already been counted
        self.counted_ids = set()

        # Total vehicles counted
        self.total_count = 0

    def update(self, track_ids):

        for track_id in track_ids:

            if track_id not in self.counted_ids:

                self.counted_ids.add(track_id)
                self.total_count += 1

        return self.total_count