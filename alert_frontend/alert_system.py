import time

# Global state for camera blackout timing
_blackout_start_time = None

def decide_alert(detection_output):
    """
    Decide ATM alert level based on detection output.
    """

    global _blackout_start_time

    # Camera blackout > 5 seconds
    if detection_output.get("camera_blackout", False):
        if _blackout_start_time is None:
            _blackout_start_time = time.time()
        elif time.time() - _blackout_start_time >= 5:
            return "HIGH_ALERT", "Camera blackout for more than 5 seconds"
    else:
        _blackout_start_time = None

    # High alert: suspicious confidence
    if detection_output.get("confidence", 1.0) < 0.3:
        return "HIGH_ALERT", "Low confidence detected"

    # Medium alert: face concealment
    if detection_output.get("helmet", False) or detection_output.get("mask", False):
        return "MEDIUM_ALERT", "Face concealment detected"

    # Medium alert: multiple people
    if detection_output.get("people_count", 1) > 1:
        return "MEDIUM_ALERT", "Multiple people detected"

    # Safe
    return "SAFE", "No threat detected"
