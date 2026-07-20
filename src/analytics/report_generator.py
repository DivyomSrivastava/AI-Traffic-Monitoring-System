import csv
import os
from datetime import datetime


class ReportGenerator:

    def __init__(self):

        self.report_folder = "reports"

        os.makedirs(
            self.report_folder,
            exist_ok=True
        )

    def generate(self, counts, density, green_time, statistics):

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename = os.path.join(
            self.report_folder,
            f"traffic_report_{timestamp}.csv"
        )

        with open(
            filename,
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow(["AI Traffic Monitoring System"])
            writer.writerow([])

            writer.writerow(["Date", datetime.now().strftime("%d-%m-%Y")])
            writer.writerow(["Time", datetime.now().strftime("%H:%M:%S")])

            writer.writerow([])

            writer.writerow(["Vehicle Type", "Count"])

            writer.writerow(["Cars", counts["Cars"]])
            writer.writerow(["Motorcycles", counts["Motorcycles"]])
            writer.writerow(["Buses", counts["Buses"]])
            writer.writerow(["Trucks", counts["Trucks"]])

            writer.writerow([])

            writer.writerow(["Total Vehicles", counts["Total"]])
            writer.writerow(["Traffic Density", density])
            writer.writerow(["Recommended Green Time", green_time])

            writer.writerow([])

            writer.writerow(["Flow Rate", statistics["Flow Rate"]])
            writer.writerow(["Peak Density", statistics["Peak Density"]])
            writer.writerow(["Elapsed Time", statistics["Elapsed Time"]])

        print(f"\nReport Saved Successfully\n{filename}")

        return filename