from ultralytics import YOLO
import glob
# Load a model
model = YOLO("yolo11n.pt")

# Train the model
train_results = model.train(
    data="coco8.yaml",  # path to dataset YAML
    epochs=50,  # number of training epochs
    imgsz=640,  # training image size
    device="cpu",  # device to run on, i.e. device=0 or device=0,1,2,3 or device=cpu
)

image_folder = "/Users/vihaankhandelwal/Point-Blue-DataGood-Project/SkuaDroneImages/"

# Get all images in the folder (assuming .jpg format; adjust as needed)
image_paths = glob.glob(image_folder + "*.jpg")

# Run the model on each image and display results
for image_path in image_paths:
    results = model(image_path)  # Run detection on the image
    results[0].show()  # Display the image with bounding boxes

# Evaluate model performance on the validation set
metrics = model.val()

for image_path in image_paths:
    results = model(image_path)  # Run detection on the image
    results[0].save(save_dir="/Users/vihaankhandelwal/data_output")  # Display the image with bounding boxes

# Export the model to ONNX format
path = model.export(format="onnx")  # return path to exported model