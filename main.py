print("RUNNING FILE:", __file__)

import cv2
from detection_model import detect_activity
from event_bus import generate_event
from alert_system import handle_event   # 👈 Hari's module

# ---------------- CAMERA SETUP ----------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not opened")
    exit()

print("Camera started, entering main loop")

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame read failed")
        break

    # 1️⃣ ML Detection
    data = detect_activity(frame)
    print("Output:", data)

    # 2️⃣ Event Generation (with cooldown)
    events = generate_event(data)

    if events:
        for event in events:
            handle_event(event)   # 🚨 ALERT SYSTEM
    else:
        print("No events triggered")

    # 3️⃣ Display Overlay
    cv2.putText(frame, f"People: {data['people_count']}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, f"Helmet: {data['helmet']}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.putText(frame, f"Mask: {data['mask']}", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.imshow("ATM AI Security - Day 5", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ---------------- CLEANUP ----------------
cap.release()
cv2.destroyAllWindows()