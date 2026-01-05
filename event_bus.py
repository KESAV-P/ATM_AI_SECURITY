import time

print("event_bus.py LOADED")

# Store last trigger times
_last_triggered = {}

COOLDOWN_SECONDS = {
    "MULTIPLE_PERSON_DETECTED": 10,
    "FACE_CONCEALMENT": 8,
    "CAMERA_TAMPERING": 5
}

def generate_event(data):
    print("generate_event() CALLED")
    events = []
    now = time.time()

    def can_trigger(event_type):
        last_time = _last_triggered.get(event_type, 0)
        cooldown = COOLDOWN_SECONDS.get(event_type, 5)
        return (now - last_time) > cooldown

    # Multiple people near ATM
    if data["people_count"] >= 3 and can_trigger("MULTIPLE_PERSON_DETECTED"):
        _last_triggered["MULTIPLE_PERSON_DETECTED"] = now
        events.append({
            "type": "MULTIPLE_PERSON_DETECTED",
            "severity": "HIGH",
            "message": f"{data['people_count']} people near ATM"
        })

    # Face concealment
    if (data["helmet"] or data["mask"]) and can_trigger("FACE_CONCEALMENT"):
        _last_triggered["FACE_CONCEALMENT"] = now
        events.append({
            "type": "FACE_CONCEALMENT",
            "severity": "MEDIUM",
            "message": "Helmet or mask detected"
        })

    # Camera blackout
    if data["camera_blackout"] and can_trigger("CAMERA_TAMPERING"):
        _last_triggered["CAMERA_TAMPERING"] = now
        events.append({
            "type": "CAMERA_TAMPERING",
            "severity": "CRITICAL",
            "message": "Camera feed blacked out"
        })

    return events