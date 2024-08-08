from ultralytics import YOLO
import glob
import random
import os

# Runs base path
run_base_path = '../runs/detect/train'
# Load a model
model = YOLO(os.path.join(run_base_path, 'weights', 'best.pt'))  # pretrained YOLOv8n model

# Run batched inference on a list of images
img_paths = glob.glob('/Users/eriksorensen/Downloads/bee_images/images/*.jpg')
random.shuffle(img_paths)
results = model(img_paths[0:10])  # return a list of Results objects

if not os.path.exists(os.path.join(run_base_path, 'img_results')):
    os.mkdir(os.path.join(run_base_path, 'img_results'))

# Process results list
i = 0
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    # result.show()  # display to screen
    result.save(filename=os.path.join(run_base_path, 'img_results', f"{os.path.basename(img_paths[i])}"))  # save to disk
    i += 1
    