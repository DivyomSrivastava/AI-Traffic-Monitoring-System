class TrafficDensity:

    def __init__(self):
        self.density = "LOW"

    def calculate(self, total_vehicles):

        if total_vehicles <= 5:
            self.density = "LOW"

        elif total_vehicles <= 10:
            self.density = "MEDIUM"

        else:
            self.density = "HIGH"

        return self.density