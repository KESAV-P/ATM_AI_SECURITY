import cv2
import numpy as np
from ultralytics import YOLO
import os

class ATMActivityDetector:
    def __init__(self):
        # 1. Person Detection Model (Standard YOLOv8)
        self.person_model = YOLO("yolov8n.pt")
        
        # 2. Helmet Detection Model (Custom)
        self.helmet_model_path = "/Users/kesavp/Projects/ATM_AI_SECURITY/models/helmet_detection/weights/best.pt"
        self.helmet_model = None
        if os.path.exists(self.helmet_model_path):
            try:
                self.helmet_model = YOLO(self.helmet_model_path)
                print(f"Loaded Custom Helmet Model: {self.helmet_model_path}")
            except Exception as e:
                print(f"Error loading helmet model: {e}")
        
        # 3. Mask Detection Model (Custom)
        self.mask_model_path = "/Users/kesavp/Projects/ATM_AI_SECURITY/models/mask/best.pt"
        self.mask_model = None
        if os.path.exists(self.mask_model_path):
            try:
                self.mask_model = YOLO(self.mask_model_path)
                print(f"Loaded Custom Mask Model: {self.mask_model_path}")
            except Exception as e:
                print(f"Error loading mask model: {e}")

    def detect(self, frame):
        # --- 1. DETECT PEOPLE ---
        person_results = self.person_model.predict(source=frame, classes=[0], conf=0.5, verbose=False)
        people_count = 0
        
        # Draw Person Boxes (Green)
        for r in person_results:
            if r.boxes:
                for box in r.boxes:
                    people_count += 1
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, "Person", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        helmet_detected = False
        mask_detected = False

        # --- 2. DETECT HELMETS (Custom Model) ---
        if self.helmet_model:
            # Increased confidence to 0.80 to avoid false positives on bare heads
            helmet_results = self.helmet_model.predict(source=frame, conf=0.80, verbose=False)
            for r in helmet_results:
                if r.boxes:
                    for box in r.boxes:
                        cls_id = int(box.cls[0])
                        class_name = self.helmet_model.names[cls_id]
                        conf = float(box.conf[0])
                        
                        # Assuming class 'With Helmet' or similar. 
                        # Update logic based on your specific training labels if needed.
                        # Usually custom datasets are: 0: With Helmet, 1: Without Helmet
                        # We trigger on 'With Helmet' or just detection if single class.
                        
                        is_helmet = False
                        if "NO" not in class_name.upper() and "WITHOUT" not in class_name.upper():
                             # Likely "Helmet" or "With Helmet"
                             is_helmet = True

                        if is_helmet:
                            helmet_detected = True
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            # Blue Box for Helmet
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                            cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # --- 3. DETECT MASKS (Custom Model) ---
        if self.mask_model:
            mask_results = self.mask_model.predict(source=frame, conf=0.6, verbose=False)
            for r in mask_results:
                if r.boxes:
                    for box in r.boxes:
                        cls_id = int(box.cls[0])
                        class_name = self.mask_model.names[cls_id]
                        conf = float(box.conf[0])
                        
                        # Logic for mask: 'With Mask' is the target.
                        is_mask = False
                        if "NO" not in class_name.upper() and "WITHOUT" not in class_name.upper():
                            is_mask = True
                        
                        if is_mask:
                            mask_detected = True
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            # Red Box for Mask
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                            cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # ---------------- CAMERA BLACKOUT ----------------
        gray_full = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray_full)
        camera_blackout = brightness < 20

        return {
            "helmet": bool(helmet_detected),
            "mask": bool(mask_detected),
            "sunglasses": False,
            "people_count": people_count,
            "camera_blackout": bool(camera_blackout),
            "confidence": 0.9
        }

# Backwards compatibility stub
_default_detector = None

def detect_activity(frame):
    global _default_detector
    if _default_detector is None:
        _default_detector = ATMActivityDetector()
    return _default_detector.detect(frame)