# ATM AI Security System 🛡️🤖

**An Intelligent Edge-AI Surveillance System for ATM Vestibules**

This project is a real-time computer vision system designed to detect security threats in ATM environments. It replaces passive CCTV recording with active prevention, instantly identifying unauthorized behavior and triggering automated responses.

## 🚀 Features

### 1. Smart Threat Detection (Multi-Model AI)
-   **Crowd Detection:** Automatically counts people to enforce "One Person at a Time" rule.
-   **Helmet Detection:** Identifies motorcycle helmets (Face Concealment compliance).
-   **Mask Detection:** Detects surgical/cloth masks (Face Concealment compliance).
-   **Tamper Detection:** Uses pixel-level analysis to detect Camera Blackouts (Sabotage/Spraying).

### 2. Automated Response System
-   **Visual HUD:** Overlays "ACCESS DENIED" or "SAFE" status directly on the monitor.
-   **Audio Alarms:** Plays loud siren sound effects (`siren.wav`) and TTS voice warnings ("Security Breach Detected").
-   **Emergency Calling:** Automatically dials the Police/Security (e.g., `7010142014`) using a connected Android phone via ADB.

## 🛠️ Tech Stack

-   **Language:** Python 3.9+
-   **Vision Config:** OpenCV (`cv2`)
-   **AI Core:** Ultralytics YOLOv8 (Nano model)
-   **Automation:** Android Debug Bridge (ADB)
-   **OS Support:** MacOS / Linux / Windows

## 📂 Project Structure

```
ATM_AI_SECURITY/
├── models/             # Custom Fine-Tuned Weights (.pt)
│   ├── helmet_detection/
│   └── mask/
├── dataset/            # Training Data configurations
├── main.py             # CORE: The main application loop
├── detection_model.py  # LOGIC: The AI Inference Engine
├── alert_system.py     # ALERT: Event logging & Calling logic
├── siren.wav           # Alarm sound file
└── security_log.csv    # Automatic Incident Audit Trail
```

## ⚙️ How to Run

### 1. Prerequisite
Ensure you have Python 3 and the dependencies installed:
```bash
pip install -r requirements.txt
```
*Required: `ultralytics`, `opencv-python`, `numpy`.*

### 2. Android Setup (For Auto-Calling)
1.  Connect Android phone via USB.
2.  Enable **USB Debugging** AND **USB Debugging (Security Settings)** in Developer Options.
3.  Ensure `adb` is installed (`brew install android-platform-tools` on Mac).

### 3. Launch System
```bash
python3 main.py
```

## 🧠 Model Logic (Accuracy Tuned)
-   **Strictness:** Helmet Detection set to **0.80 Confidence**.
-   **Persistence:** Threats must be visible for **>0.3 seconds** (6 frames) to trigger an alert, preventing false positives from flickering.

## 👥 Contributors
-   **Kesav P** – Algorithm & AI Development
-   **Hari** – Alert System & Integration