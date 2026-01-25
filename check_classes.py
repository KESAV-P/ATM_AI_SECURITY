from ultralytics import YOLO

try:
    model = YOLO("/Users/kesavp/Projects/ATM_AI_SECURITY/models/helmet_detection/weights/best.pt")
    print("Class Names:", model.names)
except Exception as e:
    print(e)
