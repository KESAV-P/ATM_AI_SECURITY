print("RUNNING FILE:", __file__)

import cv2
from detection_model import ATMActivityDetector
from event_bus import generate_event
from alert_system import handle_event

# ---- INIT DETECTOR ----
# ---- INIT DETECTOR ----
print("🔄 Initializing Detection System...")
# The detector now automatically loads the models from the predefined paths
detector = ATMActivityDetector()
print("✅ Detector Initialized")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not opened")
    exit()

print("✅ Camera started")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    data = detector.detect(frame)
    print("Output:", data)

    events = generate_event(data)
    for event in events:
        handle_event(event)

    # ---- UI ----
    cv2.putText(frame, f"People: {data['people_count']}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, f"Helmet: {data['helmet']}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.putText(frame, f"Mask: {data['mask']}", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.imshow("ATM AI Security", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()