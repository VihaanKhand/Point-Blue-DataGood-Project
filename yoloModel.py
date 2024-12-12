from ultralytics import YOLO
import os
import random


# Load the model
model = YOLO("runs/detect/train2/weights/best.pt")

# Train with optimized parameters
# model.train(
#     data='data.yaml',
#     epochs=40,              # Adjust based on validation performance
#     imgsz=640,               # Image size
#     batch=16,                # Experiment with this value
#     lr0=0.001,               # Initial learning rate
#     lrf=0.01,                # Final learning rate (optional)
#     momentum=0.937,          # Momentum for SGD
#     weight_decay=0.0005,     # Regularization term
#     save_period=10           # Save checkpoint every 10 epochs
# )





results = model.val(data="data.yaml", batch=16,  imgsz=640, save=True) 
        
# Extract metrics using the correct methods
precision = results.box.p       # Mean precision
recall = results.box.r          # Mean recall
map50 = results.box.map50        # Mean AP at IoU=0.5
#map50_95 = results.box.map()       # Mean AP at IoU=0.5:0.95

print("Precision", precision)
print("Recall", recall)
print("MAP", map50)