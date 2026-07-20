import time


class TrafficStatistics:

    def __init__(self):

        self.start_time = time.time()

        self.total_cars = 0
        self.total_motorcycles = 0
        self.total_buses = 0
        self.total_trucks = 0

        self.total_vehicles = 0

        self.peak_density = "LOW"

    def update(self, counts, density):

        self.total_cars = counts["Cars"]
        self.total_motorcycles = counts["Motorcycles"]
        self.total_buses = counts["Buses"]
        self.total_trucks = counts["Trucks"]
        self.total_vehicles = counts["Total"]

        if density == "HIGH":
            self.peak_density = "HIGH"

        elif density == "MEDIUM" and self.peak_density == "LOW":
            self.peak_density = "MEDIUM"

    def get_elapsed_time(self):

        return time.time() - self.start_time

    def get_flow_rate(self):

        elapsed_minutes = self.get_elapsed_time() / 60

        if elapsed_minutes == 0:
            return 0

        return round(self.total_vehicles / elapsed_minutes, 2)

    def get_statistics(self):

        return {
            "Cars": self.total_cars,
            "Motorcycles": self.total_motorcycles,
            "Buses": self.total_buses,
            "Trucks": self.total_trucks,
            "Total": self.total_vehicles,
            "Flow Rate": self.get_flow_rate(),
            "Peak Density": self.peak_density,
            "Elapsed Time": round(self.get_elapsed_time(), 1)
        }