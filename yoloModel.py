from ultralytics import YOLO
import os
import random
model = YOLO("runs/detect/train11/weights/best.pt")
model.train(data='data.yaml', epochs=30, imgsz=640, batch=16)
# output_directory = "/Users/sushrut.g12/Desktop/Point-Blue-DataGood-Project/InitialPredictions"
# image_folder = "/Users/sushrut.g12/Desktop/PointBlue/Point-Blue-DataGood-Project/SkuaDroneImages"
# all_images = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
# print(len(all_images))
# selected_images = random.sample(all_images, 700)


# results = model.val(data="data.yaml", batch=16,  imgsz=640, save=True) 
        
# # Extract metrics using the correct methods
# precision = results.box.p       # Mean precision
# recall = results.box.r          # Mean recall
# map50 = results.box.map50        # Mean AP at IoU=0.5
# #map50_95 = results.box.map()       # Mean AP at IoU=0.5:0.95

# print("Precision", precision)
# print("Recall", recall)
# print("MAP", map50)