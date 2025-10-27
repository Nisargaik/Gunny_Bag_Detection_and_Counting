import tkinter as tk
from gui import GunnyBagApp
from detector import Detector
from database import Database

if __name__ == "__main__":
    root = tk.Tk()
    detector = Detector("models/best.pt")  # Path to your YOLO model
    database = Database("gunnybag_counts.db")  # SQLite DB file
    app = GunnyBagApp(root, detector, database)
    root.mainloop()
