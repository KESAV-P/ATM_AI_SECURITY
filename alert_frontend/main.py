from detection_model import detect_activity
from alert_system import decide_alert
from frontend import ATMUI
import cv2

def main():
    ui = ATMUI()
    cap = cv2.VideoCapture(0)

    def loop():
        ret, frame = cap.read()
        if not ret:
            return

        detection_output = detect_activity(frame)
        alert_level, reason = decide_alert(detection_output)

        if alert_level == "SAFE":
            ui.show_safe()
        else:
            ui.show_alert(alert_level, reason)

        ui.root.after(1000, loop)

    loop()
    ui.start()
    cap.release()

if __name__ == "__main__":
    main()
