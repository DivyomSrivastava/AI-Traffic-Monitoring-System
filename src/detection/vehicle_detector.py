import cv2
from ultralytics import YOLO

from utils.constants import VEHICLE_CLASSES


def run_vehicle_detector():

    print("Loading YOLO model...")

    model = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture("assets/videos/traffic4.mp4")

    if not cap.isOpened():
        print("Error: Unable to open video.")
        return

    while True:

        success, frame = cap.read()

        if not success:
            break

        # Detect only vehicles
        results = model(frame, classes=VEHICLE_CLASSES)

        # Draw detections
        annotated_frame = results[0].plot()

        cv2.imshow("AI Traffic Monitoring System", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()