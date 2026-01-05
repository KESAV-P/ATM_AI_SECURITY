import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 nano (lightweight, edge-friendly)
model = YOLO("yolov8n.pt")

def detect_activity(frame):
    results = model.predict(source=frame, conf=0.4, verbose=False)

    people = 0
    helmet_detected = False
    mask_detected = False

    h, w, _ = frame.shape

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            # Person class
            if cls == 0 and conf > 0.5:
                people += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # ---------------- HELMET DETECTION ----------------
                # Head region = top 25% of person bounding box
                head_y2 = y1 + int(0.25 * (y2 - y1))
                head_region = frame[y1:head_y2, x1:x2]

                if head_region.size > 0:
                    hsv = cv2.cvtColor(head_region, cv2.COLOR_BGR2HSV)

                    # Yellow & white helmet color ranges
                    mask_yellow = cv2.inRange(hsv, (15, 80, 80), (40, 255, 255))
                    mask_white = cv2.inRange(hsv, (0, 0, 220), (180, 40, 255))

                    helmet_score = np.mean(mask_yellow) + np.mean(mask_white)

                    if helmet_score > 25:   # tightened threshold
                        helmet_detected = True

                # ---------------- MASK DETECTION ----------------
                # Face region = upper-middle part of body
                face_y1 = y1 + int(0.18 * (y2 - y1))
                face_y2 = y1 + int(0.45 * (y2 - y1))
                face_region = frame[face_y1:face_y2, x1:x2]

                if face_region.size > 0:
                    gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, 50, 150)

                    # Mask reduces edges + require strong person confidence
                    if np.mean(edges) < 15 and conf > 0.6:
                        mask_detected = True

    # ---------------- CAMERA BLACKOUT ----------------
    gray_full = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray_full)
    camera_blackout = brightness < 20

    # Safety: if no people, no helmet/mask
    if people == 0:
        helmet_detected = False
        mask_detected = False

    return {
        "helmet": bool(helmet_detected),
        "mask": bool(mask_detected),
        "sunglasses": False,   # Day 4
        "people_count": people,
        "camera_blackout": bool(camera_blackout),
        "confidence": 0.9
    }