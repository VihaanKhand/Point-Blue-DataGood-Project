
from ultralytics import YOLO
import os
import random


# Load the model
model = YOLO("runs/detect/train3/weights/best.pt")


results = model.val(data="data.yaml", batch=16,  imgsz=640, save=True, save_conf = True) 
        
# Extract metrics using the correct methods
precision = results.box.p       # Mean precision
recall = results.box.r          # Mean recall
map50 = results.box.map50        # Mean AP at IoU=0.5
#map50_95 = results.box.map()       # Mean AP at IoU=0.5:0.95

print("Precision", precision)
print("Recall", recall)
print("MAP", map50)

