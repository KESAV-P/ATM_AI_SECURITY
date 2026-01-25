from ultralytics import YOLO

def resume_training():
    # Path to the last checkpoint
    checkpoint_path = "/Users/kesavp/Projects/ATM_AI_SECURITY/models/helmet_detection/weights/last.pt"
    
    print(f"Resuming training from: {checkpoint_path}")
    
    try:
        model = YOLO(checkpoint_path)
        model.train(resume=True, device='mps')
    except FileNotFoundError:
        print(f"Error: Checkpoint not found at {checkpoint_path}")
        print("Required file 'last.pt' does not exist yet. Did the training run long enough to save a specific epoch?")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    resume_training()
