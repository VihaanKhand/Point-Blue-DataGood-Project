from ultralytics import YOLO
import os
import random


# Load the model
model = YOLO("runs/detect/train3/weights/best.pt")

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

# Train with optimized parameters
model.train(
    data='data.yaml',            # Dataset configuration
    epochs=45,                  # Train for 100 epochs
    imgsz=640,                   # Image size
    batch=16,                    # Batch size (increase if GPU allows)
    lr0=0.001,                   # Initial learning rate
    lrf=0.01,                    # Final learning rate
    momentum=0.937,              # Momentum
    weight_decay=0.0005,         # Regularization
    conf=0.7,                   # Confidence threshold
    iou=0.5,                     # IoU threshold for NMS
    save_period=10,              # Save checkpoints every 10 epochs
)
