from ultralytics import YOLO
import os

def train_model():
    # Load a model
    model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

    # Train the model
    # We use the absolute path to data.yaml
    data_path = "/Users/kesavp/Projects/ATM_AI_SECURITY/data/raw/helmet_dataset/data.yaml"
    
    print(f"Starting training with dataset: {data_path}")
    
    results = model.train(
        data=data_path, 
        epochs=50, 
        imgsz=640, 
        project="/Users/kesavp/Projects/ATM_AI_SECURITY/models",
        name="helmet_detection",
        exist_ok=True,
        device="mps"
    )
    
    print("Training complete.")
    print(f"Best model saved at: {results.save_dir}/weights/best.pt")

if __name__ == '__main__':
    train_model()
