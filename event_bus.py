import time

_last_event_time = {}
EVENT_COOLDOWN = 8  # seconds


def can_trigger(event_type):
    now = time.time()
    last = _last_event_time.get(event_type, 0)
    if now - last > EVENT_COOLDOWN:
        _last_event_time[event_type] = now
        return True
    return False


def generate_event(data):
    events = []

    if (data["helmet"] or data["mask"]) and can_trigger("FACE_CONCEALMENT"):
        events.append({
            "type": "FACE_CONCEALMENT",
            "severity": "MEDIUM",
            "message": "Helmet or mask detected"
        })

    if data["people_count"] > 1 and can_trigger("MULTIPLE_PEOPLE"):
        events.append({
            "type": "MULTIPLE_PEOPLE",
            "severity": "HIGH",
            "message": "More than one person detected"
        })

    if data["camera_blackout"] and can_trigger("CAMERA_TAMPERING"):
        events.append({
            "type": "CAMERA_TAMPERING",
            "severity": "CRITICAL",
            "message": "Camera feed blacked out"
        })

    return events