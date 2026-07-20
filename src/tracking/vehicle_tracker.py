import cv2
from ultralytics import YOLO

from analytics.traffic_density import TrafficDensity
from analytics.line_counter import LineCounter
from analytics.signal_controller import SignalController
from analytics.traffic_statistics import TrafficStatistics

from utils.constants import (
    VEHICLE_CLASSES,
    CLASS_NAMES,
    LINE_POSITION,
    LINE_COLOR,
    LINE_THICKNESS,
    BOX_COLOR,
    BOX_THICKNESS,
    TEXT_COLOR,
)

def run_vehicle_tracker():

    print("Loading YOLO Tracker...")

    # Load YOLO Model
    MODEL_PATH = "models/yolov8n.pt"
    model = YOLO(MODEL_PATH)

    # Load Video
    cap = cv2.VideoCapture("assets/videos/traffic4.mp4")

    if not cap.isOpened():
        print("Error opening video.")
        return

    line_counter = None
    density_calculator = TrafficDensity()
    statistics = TrafficStatistics()
    signal_controller = SignalController()
    while True:

        success, frame = cap.read()

        if not success:
            break

        height, width = frame.shape[:2]
        line_y = int(height * LINE_POSITION)

        if line_counter is None:
            line_counter = LineCounter(line_y)

        # Run YOLO + ByteTrack
        results = model.track(
            frame,
            classes=VEHICLE_CLASSES,
            persist=True,
            verbose=False,
        )

        annotated_frame = frame.copy()

        # Draw Counting Line
        cv2.line(
            annotated_frame,
            (0, line_y),
            (width, line_y),
            LINE_COLOR,
            LINE_THICKNESS,
        )

        cv2.putText(
            annotated_frame,
            "COUNTING LINE",
            (20, line_y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            LINE_COLOR,
            2,
        )

        # Process detections
        if (
            results
            and results[0].boxes is not None
            and results[0].boxes.id is not None
        ):

            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)
            class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
            confidences = results[0].boxes.conf.cpu().numpy()

            for box, track_id, class_id, confidence in zip(
                boxes,
                track_ids,
                class_ids,
                confidences,
            ):

                x1, y1, x2, y2 = map(int, box)

                # Vehicle Center
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                # Update Counter
                line_counter.update(
                    track_id,
                    class_id,
                    center_y,
                )

                # Bounding Box
                cv2.rectangle(
                    annotated_frame,
                    (x1, y1),
                    (x2, y2),
                    BOX_COLOR,
                    BOX_THICKNESS,
                )

                # Center Point
                cv2.circle(
                    annotated_frame,
                    (center_x, center_y),
                    4,
                    (0, 255, 255),
                    -1,
                )

                class_name = CLASS_NAMES.get(class_id, "Vehicle")

                label = f"{class_name} #{track_id} {confidence:.2f}"

                # Label Background
                cv2.rectangle(
                    annotated_frame,
                    (x1, y1 - 25),
                    (x1 + 180, y1),
                    BOX_COLOR,
                    -1,
                )

                # Label
                cv2.putText(
                    annotated_frame,
                    label,
                    (x1 + 5, y1 - 7),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    TEXT_COLOR,
                    2,
                )

        # Get Counts
        counts = line_counter.get_counts()

        # Calculate Density
        density = density_calculator.calculate(
            counts["Total"]
        )
        statistics.update(counts, density)
        traffic_stats = statistics.get_statistics()
        green_time = signal_controller.get_signal_time(density)
        recommendation = signal_controller.get_recommendation(density)

        # Dashboard Background
        cv2.rectangle(
            annotated_frame,
            (10, 10),
            (500, 420),
            (40, 40, 40),
            -1,
        )

        # Dashboard Title
        cv2.putText(
            annotated_frame,
            "TRAFFIC ANALYTICS",
            (25, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2,
        )

        # Dashboard Values
        cv2.putText(
            annotated_frame,
            f"Cars         : {counts['Cars']}",
            (25, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            annotated_frame,
            f"Motorcycles  : {counts['Motorcycles']}",
            (25, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            annotated_frame,
            f"Buses        : {counts['Buses']}",
            (25, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            annotated_frame,
            f"Trucks       : {counts['Trucks']}",
            (25, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            annotated_frame,
            f"Total        : {counts['Total']}",
            (25, 195),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 0),
            2,
        )

        cv2.putText(
            annotated_frame,
            f"Density      : {density}",
            (25, 225),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 255),
            2,
        )
        # Green Time
        cv2.putText
        (
            annotated_frame,
            f"Green Time  : {green_time} sec",
            (25, 255),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.70,
            (0, 255, 255),
            2,
        )
        # Recommendation
        cv2.putText(
            annotated_frame,
            "Recommendation:",
            (25, 285),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            annotated_frame,
            f"{recommendation}",
            (40, 310),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.60,
            (0, 255, 0),
            2,
        )
        
   

        # Traffic Statistics
        cv2.putText(
            annotated_frame,
            f"Flow Rate : {traffic_stats['Flow Rate']} veh/min",
            (25, 340),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.60,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            annotated_frame,
            f"Peak Density : {traffic_stats['Peak Density']}",
            (25, 365),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.60,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            annotated_frame,
            f"Elapsed : {traffic_stats['Elapsed Time']} sec",
            (25, 390),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.60,
            (255, 255, 255),
            2,
        )


        # Display Window
        cv2.imshow(
            "AI Traffic Monitoring System",
            annotated_frame,            
        )

        # Exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_vehicle_tracker()