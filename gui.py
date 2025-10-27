import tkinter as tk
from tkinter import filedialog, messagebox,ttk
from PIL import Image, ImageTk
import os

class GunnyBagApp:
    def __init__(self, root, detector, database):
        self.root = root
        self.root.title("Gunny Bag Detection and Counting")
        self.root.geometry("1200x800")
        
        self.bg_color = "#aac0d7"       # light gray/white main background
        

        self.root.configure(bg=self.bg_color)

        """self.header = tk.Canvas(root, height=50, bg="#aac0d7")
        self.header.pack(fill="x")

        steps = 100
        for i in range(steps):
            r = int(i / steps * 255)
            color = f"#{(107 - i//2):02x}{(184 - i//3):02x}{(255 - i//4):02x}"
            self.header.create_rectangle((i*9, 0, (i+1)*9, 60), outline="", fill=color)"""

        # --- Top frame for buttons ---
        button_frame = tk.Frame(root, bg=self.bg_color)
        button_frame.pack(pady=15)

        # Upload button
        self.upload_btn = tk.Button(
            button_frame, text="Select Image", command=self.upload_file,
            bg="#0077cc", fg="white", font=("Arial", 12, "bold"),
            width=15, relief="flat"
        )
        self.upload_btn.grid(row=0, column=0, padx=10)

        # Run detection button
        self.detect_btn = tk.Button(
            button_frame, text="Run Detection", command=self.run_detection,
            bg="#28a745", fg="white", font=("Arial", 12, "bold"),
            width=15, relief="flat"
        )
        self.detect_btn.grid(row=0, column=1, padx=10)

        # Show history button
        self.history_btn = tk.Button(
            button_frame, text="Show History", command=self.show_history,
            bg="#ff9800", fg="white", font=("Arial", 12, "bold"),
            width=15, relief="flat"
        )
        self.history_btn.grid(row=0, column=2, padx=10)

        # --- Label to show image ---
        self.image_label = tk.Label(root, bg=self.bg_color)
        self.image_label.pack(pady=15)

        # --- Count display ---
        self.count_label = tk.Label(
            root, text="Count: 0", font=("Arial", 16, "bold"),
            bg=self.bg_color, fg="#333"
        )
        self.count_label.pack(pady=10)

        self.detector = detector
        self.database = database
        self.file_path = None

    def upload_file(self):
        self.file_path = filedialog.askopenfilename(
            initialdir=os.path.join(os.getcwd(),"images"),
            filetypes=[("Image/Video files", "*.jpg *.png *.jpeg *.mp4 *.avi")]
        )
        if self.file_path:
            messagebox.showinfo("File Selected", f"File: {self.file_path}")

    def run_detection(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please upload a file first!")
            return

        result_img_path, count = self.detector.run(self.file_path)

        # Display result
        img = Image.open(result_img_path)
        img = img.resize((600, 400))
        img = ImageTk.PhotoImage(img)
        self.image_label.config(image=img)
        self.image_label.image = img

        # Update count label
        self.count_label.config(text=f"Count: {count}")

        # Save count to DB
        image_name = os.path.basename(self.file_path)
        self.database.save_count(image_name, count)

    def show_history(self):
        # Create a new popup window
           history_win = tk.Toplevel(self.root)
           history_win.title("Detection History")
           history_win.geometry("600x350")

        # Table (Treeview)
           cols = ("Image", "Count", "Date", "Time")
           tree = ttk.Treeview(history_win, columns=cols, show="headings")
           tree.heading("Image", text="Image Name")
           tree.heading("Count", text="Count")
           tree.heading("Date", text="Date")
           tree.heading("Time", text="Time")

           tree.column("Image", width=200)
           tree.column("Count", width=80, anchor="center")
           tree.column("Date", width=150, anchor="center")
           tree.column("Time", width=150, anchor="center")

           tree.pack(fill="both", expand=True)

        # Fetch data from DB
           records = self.database.get_history()  
        # records should now return tuples like: (image_name, count, date)

           for row in records:
             tree.insert("", "end", values=row)

        # Add scrollbar
           scrollbar = ttk.Scrollbar(history_win, orient="vertical", command=tree.yview)
           tree.configure(yscroll=scrollbar.set)
           scrollbar.pack(side="right", fill="y")



    