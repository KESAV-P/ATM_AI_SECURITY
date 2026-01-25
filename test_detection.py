import cv2
import numpy as np
from detection_model import detect_activity

# Create a dummy image
img = np.zeros((480, 640, 3), dtype=np.uint8)

# Run detection
try:
    print("Running detection...")
    result = detect_activity(img)
    print("Detection successful!")
    print("Result:", result)
except Exception as e:
    print("Detection failed:")
    print(e)
