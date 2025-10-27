import pathlib
# Fix path issues when loading models trained on Linux/Colab
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

from ultralytics import YOLO
import os

class Detector:
    def __init__(self, model_path="models/best.pt"):
        # Load YOLOv8 trained model
        self.model = YOLO(model_path)

    def run(self, file_path):
        # Run detection, auto-save results
        results = self.model(file_path, save=True, project="runs/detect", name="predict", exist_ok=True)

        # Number of detections
        count = len(results[0].boxes)

        # YOLOv8 stores image path in results[0].path
        result_img_path = os.path.join("runs/detect/predict", os.path.basename(file_path))  

        return result_img_path, count
