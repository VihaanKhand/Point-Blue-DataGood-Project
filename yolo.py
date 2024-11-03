from ultralytics import YOLO
import glob
import os
import cv2

# Load a pre-trained model
model = YOLO('yolov8n.pt')  # 'yolov8n.pt' is a pre-trained YOLOv8 nano model

model.train(data='/path/to/Point-Blue-DataGood-Project/data.yaml', epochs=100, imgsz=640)

# Define input and output folders
image_folder = "SkuaDroneImages/"
output_folder = os.path.expanduser("~/data_output/")
os.makedirs(output_folder, exist_ok=True)

# Get all images in the folder (assuming .jpg format; adjust as needed)
image_paths = glob.glob(image_folder + "*.jpg")
print("Image paths:", image_paths)  # Check if images are found

# Run inference on each image and save results
for image_path in image_paths:
    results = model.predict(image_path)  # Run detection on the image

    for result in results:
        # Get image with bounding boxes drawn
        annotated_image = result.plot()
        if annotated_image is not None:
            output_path = os.path.join(output_folder, os.path.basename(image_path))
            cv2.imwrite(output_path, annotated_image)
            print(f"Saved annotated image to {output_path}")
        else:
            print(f"No annotated image for {image_path}")

# Evaluate model performance on the validation set (optional)
metrics = model.val()

# Optionally, export the model to ONNX format
path = model.export(format="onnx")  # returns path to exported model