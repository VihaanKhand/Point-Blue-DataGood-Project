from ultralytics import YOLO
import os
import time
from PIL import Image

# Function to process images in batches
def process_images_in_batches(image_paths, batch_size=20):
    results = []
    for i in range(0, len(image_paths), batch_size):
        batch = image_paths[i:i + batch_size]
        print(f"Processing batch {i // batch_size + 1} of {len(image_paths) // batch_size + 1}")
        
        # Run prediction on the current batch without saving automatically
        batch_results = model.predict(source=batch, save=False, save_txt=True, save_conf=False, save_crop=True,iou=0.5, conf=0.6)
        
        # Check if there are any detections (bounding boxes) and save the image if detections exist
        for result in batch_results:
            if len(result.boxes) > 0:  # If bounding boxes are detected
                result.save()  # Save the image with bounding boxes
                print(f"Saved image: {result.path}")
            else:
                print(f"No bounding boxes for image: {result.path}, skipping save.")
        
        results.extend(batch_results)  # Collect all results
        time.sleep(1)  # Optional: Add a small delay between batches to manage system load
        
    return results

# Load your trained model
model = YOLO("runs/detect/train12/weights/best.pt")

# Path to your larger dataset of unlabeled images
unlabeled_image_folder = "sampledImages"
all_images = [os.path.join(unlabeled_image_folder, f) for f in os.listdir(unlabeled_image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

# Directory to save the predictions
output_directory = "data_output"

# Process the images in batches to avoid opening too many files at once
results = process_images_in_batches(all_images, batch_size=100)

print("Predictions saved!")
