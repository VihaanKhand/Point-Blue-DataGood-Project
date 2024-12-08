import os
import random
from ultralytics import YOLO

# Define parameters programmatically
params = {
    "weights": "/runs/detect/train8/weights/best.pt",
    "image_folder": "Point-Blue-DataGood-Project/SkuaDroneImages",
    "data_yaml": "datageneral.yaml",
    "epochs": 10,
    "imgsz": 640,
    "batch": 16,
    "sample_size": 700,
}

# Load the YOLO model
if not os.path.isfile(params["weights"]):
    raise FileNotFoundError(f"Weights file not found: {params['weights']}")
model = YOLO(params["weights"])

# Train the model
if os.path.isfile(params["data_yaml"]):  # Ensure the YAML file exists
    print(f"Training the model with data: {params['data_yaml']}, epochs: {params['epochs']}, imgsz: {params['imgsz']}, batch: {params['batch']}")
    model.train(data=params["data_yaml"], epochs=params["epochs"], imgsz=params["imgsz"], batch=params["batch"])
else:
    print(f"Skipping training since data YAML file is missing: {params['data_yaml']}")

# Verify the image folder exists
if not os.path.isdir(params["image_folder"]):
    raise NotADirectoryError(f"Image folder not found: {params['image_folder']}")

# Collect all image files
all_images = [
    os.path.join(params["image_folder"], f)
    for f in os.listdir(params["image_folder"])
    if f.endswith(('.jpg', '.jpeg', '.png'))
]
print(f"Total images found: {len(all_images)}")

# Ensure there are enough images for sampling
if len(all_images) < params["sample_size"]:
    raise ValueError(f"Not enough images in the folder ({len(all_images)} available, {params['sample_size']} needed).")

# Randomly sample images for prediction
selected_images = random.sample(all_images, params["sample_size"])

# Use the model to predict on the selected images
results = model.predict(source=selected_images)

# Save predictions
for result in results:
    result.save()  # Saves each result in a `runs/predict` subfolder by default

print("Predictions completed and saved!")
