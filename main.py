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
            else:
                stop_alarm()
            
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

import subprocess

# Global variables to manage alarm state and process
_alarm_active = False
_siren_proc = None
_call_made = False

def make_android_call():
    """
    Attempts to initiate a call on a connected Android device via ADB.
    Requires: 'adb' installed and a phone connected with USB Debugging enabled.
    """
    police_number = "+917010142014"  # Sync with target police number
    adb_path = "/Users/kesavp/Library/Android/sdk/platform-tools/adb"
    
    print(f"📞 Attempting to call {police_number} via Android ADB...")
    print("ℹ️  REDMI USERS: Enable 'USB Debugging (Security Settings)' in Developer Options!")
    
    try:
        # Check if device is connected first
        res = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
        lines = [line.strip() for line in res.stdout.splitlines() if line.strip()]
        devices = [line for line in lines[1:] if "device" in line and "emulator" not in line]
        if not devices:
            print("⚠️ WARNING: No Android device detected via USB debugging. Please connect a device and check screen for USB Debugging permission.")
            return

        # Try direct call (ACTION_CALL) first
        cmd_direct = f"{adb_path} shell am start -a android.intent.action.CALL -d tel:{police_number}"
        res_call = subprocess.run(cmd_direct, shell=True, capture_output=True, text=True)
        if "SecurityException" not in res_call.stderr and "Error" not in res_call.stderr:
            print("✅ Direct call initiated (android.intent.action.CALL).")
            return

        print("🔄 Direct call failed (SecurityException). Falling back to ACTION_DIAL and key emulation...")
        
        # Fallback: Open Dialer (Pre-fill number)
        cmd_dial = f"{adb_path} shell am start -a android.intent.action.DIAL -d tel:{police_number}"
        subprocess.run(cmd_dial, shell=True, capture_output=True, text=True)
        time.sleep(2)
        
        # Try TAB twice to focus button (Redmi specific)
        cmd_tab = f"{adb_path} shell input keyevent 61"
        subprocess.run(cmd_tab, shell=True, capture_output=True, text=True)
        subprocess.run(cmd_tab, shell=True, capture_output=True, text=True)
        
        # Press ENTER
        cmd_enter = f"{adb_path} shell input keyevent 66"
        subprocess.run(cmd_enter, shell=True, capture_output=True, text=True)
        
        # Press CALL (Backup)
        cmd_call = f"{adb_path} shell input keyevent 5"
        subprocess.run(cmd_call, shell=True, capture_output=True, text=True)
        
        print("✅ Call initiated via dialer fallback (Keys Sent).")
            
    except Exception as e:
        print(f"❌ ADB Execution Error: {e}")

def play_alarm():
    """Plays a system alert sound in a separate thread and allows immediate stopping."""
    global _alarm_active, _call_made
    
    # 1. Trigger the Phone Call (once per alert session)
    if not _call_made:
        _call_made = True
        t_call = threading.Thread(target=make_android_call)
        t_call.daemon = True
        t_call.start()
        
    if _alarm_active:
        return
    _alarm_active = True

    def _sound_loop():
        global _alarm_active, _siren_proc
        
        # 2. Play the downloaded siren sound (Smoke Detector/Alarm style)
        for _ in range(3):
            if not _alarm_active:
                break
            try:
                _siren_proc = subprocess.Popen(["afplay", "siren.wav"])
                _siren_proc.wait()
            except Exception as e:
                print(f"Error playing sound: {e}")
                break
        
        # 3. Voice announcement
        if _alarm_active:
            try:
                _siren_proc = subprocess.Popen(["say", "Security Breach Detected. Police have been notified."])
                _siren_proc.wait()
            except Exception as e:
                pass
        
        _alarm_active = False
        _siren_proc = None

    t_sound = threading.Thread(target=_sound_loop)
    t_sound.daemon = True
    t_sound.start()

def stop_alarm():
    """Immediately stops any playing siren or voice processes and resets call status."""
    global _alarm_active, _siren_proc, _call_made
    _alarm_active = False
    _call_made = False
    
    if _siren_proc is not None:
        try:
            _siren_proc.kill()
            _siren_proc.wait(timeout=1)
        except Exception:
            pass
        _siren_proc = None
        
    # Force kill any residual audio/voice processes to be absolutely sure
    try:
        subprocess.run(["killall", "afplay"], capture_output=True)
        subprocess.run(["killall", "say"], capture_output=True)
    except Exception:
        pass

if __name__ == "__main__":
    main()