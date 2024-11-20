from ultralytics import YOLO
import os
import random
model = YOLO('/Users/sushrut.g12/Desktop/PointBlue/Point-Blue-DataGood-Project/runs/detect/train8/weights/best.pt')

#model.train(data='data.yaml', epochs=10, imgsz=640, batch=16)

image_folder = "/Users/sushrut.g12/Desktop/PointBlue/Point-Blue-DataGood-Project/SkuaDroneImages"
all_images = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
print(len(all_images))
selected_images = random.sample(all_images, 700)

results = model.predict(source= selected_images)

# for result in results:
#     result.save()  # Saves each result in a `runs/predict` subfolder by default
