import cv2
import numpy as np
from detection_model import detect_activity
from alert_system import decide_alert

def draw_ui(frame, alert_level, reason):
    """
    Draws the UI overlay directly on the OpenCV frame.
    """
    height, width, _ = frame.shape
    
    # 1. SAFE STATE
    if alert_level == "SAFE":
        # Green header
        cv2.rectangle(frame, (0, 0), (width, 80), (0, 255, 0), -1)
        cv2.putText(frame, "ATM STATUS: SAFE", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Bottom instruction
        cv2.putText(frame, "Please Insert Card", (20, height - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # 2. MEDIUM ALERT (Access Denied)
    elif alert_level == "MEDIUM_ALERT":
        # Orange/Red overlay (semi-transparent)
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, height), (0, 165, 255), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
        # Header
        cv2.rectangle(frame, (0, 0), (width, 100), (0, 100, 255), -1)
        cv2.putText(frame, "ACCESS DENIED", (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        
        # Reason
        cv2.putText(frame, f"Reason: {reason}", (20, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        cv2.putText(frame, "Please resolve to continue.", (20, height - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # 3. HIGH ALERT (Security Breach)
    elif alert_level == "HIGH_ALERT":
        # Full Red flash effect could be added here, strict red for now
        cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), -1)
        
        cv2.putText(frame, "CRITICAL SECURITY ALERT", (50, height//2 - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 4)
        
        cv2.putText(frame, reason.upper(), (50, height//2 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        cv2.putText(frame, "POLICE NOTIFIED", (50, height//2 + 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

    return frame

def main():
    print("🚀 Starting ATM Security System (OpenCV UI)...")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Could not open camera.")
        return

    # Set camera resolution (optional, for better UI fit)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to grab frame.")
                break

            # 1. Run AI Detection
            data = detect_activity(frame)
            
            # 2. Decide Alert Level
            alert_level, reason = decide_alert(data)
            
            # TRIGGER ALARM SOUND ON HIGH ALERT
            if alert_level == "HIGH_ALERT":
                play_alarm()
            
            # 3. Draw UI
            frame = draw_ui(frame, alert_level, reason)
            
            # 4. Show Display
            cv2.imshow("ATM AI Security System", frame)
            
            # Quit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        cap.release()
        cv2.destroyAllWindows()

import os
import threading
import time

# Global variable to manage alarm thread
_alarm_playing = False

def play_alarm():
    """Plays a system alert sound in a separate thread to avoid blocking UI."""
    global _alarm_playing
    if _alarm_playing:
        return

    def _sound_loop():
        global _alarm_playing
        _alarm_playing = True
        
        # Play the downloaded siren sound (Smoke Detector/Alarm style)
        for _ in range(3):
            os.system("afplay siren.wav")
        
        # Voice announcement
        os.system("say 'Security Breach Detected.'")
        
        _alarm_playing = False

    t = threading.Thread(target=_sound_loop)
    t.daemon = True
    t.start()

if __name__ == "__main__":
    main()