class SignalController:

    def __init__(self):
        pass

    def get_signal_time(self, density):

        if density == "LOW":
            return 20

        elif density == "MEDIUM":
            return 40

        elif density == "HIGH":
            return 60

        elif density == "VERY HIGH":
            return 90

        return 30

    def get_recommendation(self, density):

        if density == "LOW":
            return "Normal Flow"

        elif density == "MEDIUM":
            return "Increase Green Time"

        elif density == "HIGH":
            return "Extend Green Phase"

        elif density == "VERY HIGH":
            return "Critical Congestion"

        return "Unknown"