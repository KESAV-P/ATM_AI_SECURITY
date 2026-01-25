from ultralytics import YOLO

def train_mask_model():
    # Load a model
    model = YOLO("yolov8n.pt")  # load a pretrained model

    # Train the model
    data_path = "/Users/kesavp/Projects/ATM_AI_SECURITY/dataset/data.yaml"
    
    print(f"Starting MASK training with dataset: {data_path}")
    
    results = model.train(
        data=data_path, 
        epochs=50, 
        imgsz=640, 
        project="/Users/kesavp/Projects/ATM_AI_SECURITY/models",
        name="mask_detection",
        exist_ok=True,
        device="mps"  # Use Mac GPU
    )
    
    print("Mask Training complete.")
    print(f"Best model saved at: {results.save_dir}/weights/best.pt")

if __name__ == '__main__':
    train_mask_model()
