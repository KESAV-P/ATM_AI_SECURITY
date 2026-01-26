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
                
        # Stabilization Counters (Debounce)
        self.helmet_counter = 0
        self.mask_counter = 0

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

        raw_helmet_detected = False
        if self.helmet_model:
            # STRICT MODE: Confidence 0.80 (Balanced)
            helmet_results = self.helmet_model.predict(source=frame, conf=0.80, verbose=False)
            for r in helmet_results:
                if r.boxes:
                    for box in r.boxes:
                        cls_id = int(box.cls[0])
                        conf = float(box.conf[0])
                        if cls_id == 0:
                            # Verify box size to avoid tiny background clusters
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            box_h = y2 - y1
                            
                            # Size Check: Helmet must be at least 15% of screen height
                            if box_h > frame.shape[0] * 0.15:
                                raw_helmet_detected = True
                                # Blue Box
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                                cv2.putText(frame, f"HELMET {conf:.2f}", (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                                print(f"⚠️ Possible Helmet Detected: Conf={conf:.2f}")

        # Persistence Logic for Helmet (Slower build-up, faster decay)
        if raw_helmet_detected:
            self.helmet_counter = min(self.helmet_counter + 1, 15) # Cap at 15
        else:
            self.helmet_counter = max(self.helmet_counter - 2, 0) # Decay twice as fast

        # Trigger only if consistent for 6+ frames (Very stable)
        helmet_confirmed = self.helmet_counter > 6

        # --- 3. DETECT MASKS (Custom Model) ---
        raw_mask_detected = False
        if self.mask_model:
            mask_results = self.mask_model.predict(source=frame, conf=0.6, verbose=False)
            for r in mask_results:
                if r.boxes:
                    for box in r.boxes:
                        cls_id = int(box.cls[0])
                        class_name = self.mask_model.names[cls_id]
                        
                        is_mask = False
                        if "NO" not in class_name.upper() and "WITHOUT" not in class_name.upper():
                            is_mask = True
                        
                        if is_mask:
                            raw_mask_detected = True
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            # Red Box
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                            cv2.putText(frame, f"MASK", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Persistence Logic for Mask
        if raw_mask_detected:
            self.mask_counter = min(self.mask_counter + 1, 10)
        else:
            self.mask_counter = max(self.mask_counter - 1, 0)
            
        mask_confirmed = self.mask_counter > 3

        # ---------------- CAMERA BLACKOUT ----------------
        gray_full = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray_full)
        camera_blackout = brightness < 20

        return {
            "helmet": bool(helmet_confirmed),
            "mask": bool(mask_confirmed),
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