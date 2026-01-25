from pathlib import Path
import shutil

RAW = Path("../data/raw")
PROCESSED = Path("../data/processed")

PROCESSED.mkdir(parents=True, exist_ok=True)

for img in RAW.glob("*"):
    if img.suffix.lower() in [".jpg", ".png", ".jpeg"]:
        shutil.copy(img, PROCESSED / img.name)

print("✅ Dataset prepared")