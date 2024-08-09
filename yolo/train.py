from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

if __name__ == '__main__':
    # Train the model
    results = model.train(
        data="dataset.yaml", 
        epochs=100, 
        imgsz=640, 
        batch=-1, # Auto size based on 60% memory utilization, can set to float to customize memory utilization
        device=0, # Set to train on GPU (1) or CPU (None)
    )