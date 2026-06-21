import time
import csv
import os
from datetime import datetime

# Global state for camera blackout timing
_blackout_start_time = None
LOG_FILE = "security_log.csv"

def log_event(level, reason):
    """Logs the alert to the CSV file."""
    try:
        file_exists = os.path.isfile(LOG_FILE)
        with open(LOG_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Timestamp", "Type", "Severity", "Message"])
            
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ALERT",
                level,
                reason
            ])
    except Exception as e:
        print(f"⚠️ Failed to log: {e}")

def decide_alert(detection_output):
    """
    Decide ATM alert level based on detection output.
    Returns: (AlertLevel, Reason)
    """
    global _blackout_start_time

    # 1. CRITICAL: Camera Blackout (> 3 seconds)
    if detection_output.get("camera_blackout", False):
        if _blackout_start_time is None:
            _blackout_start_time = time.time()
        
        elapsed = time.time() - _blackout_start_time
        if elapsed > 3:
            reason = f"Camera blackout detected for {int(elapsed)}s"
            log_event("HIGH", reason)
            return "HIGH_ALERT", reason
    else:
        _blackout_start_time = None

    # 2. MILD: Face Concealment (Helmet, Mask, Sunglasses)
    reasons = []
    if detection_output.get("helmet", False):
        reasons.append("Helmet detected")
    if detection_output.get("mask", False):
        reasons.append("Mask detected")
    if detection_output.get("sunglasses", False):
        reasons.append("Sunglasses detected")
    
    # 3. MILD: Multiple People
    if detection_output.get("people_count", 0) > 1:
        reasons.append("Multiple people detected")

    if reasons:
        full_reason = ", ".join(reasons)
        # We don't necessarily log every single frame of a mild alert to avoid spam,
        # but for now, we can just return it.
        return "MEDIUM_ALERT", full_reason

    # 4. SAFE
    return "SAFE", "No threat detected"