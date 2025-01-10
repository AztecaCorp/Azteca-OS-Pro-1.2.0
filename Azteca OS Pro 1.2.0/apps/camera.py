import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os

# Create the main window for the Camera and Photo Viewer App
class CameraPhotoViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera and Photo Viewer")
        self.root.geometry("800x600")
        
        # Create a folder to store captured images
        self.photos_folder = "photos"
        if not os.path.exists(self.photos_folder):
            os.makedirs(self.photos_folder)

        # Initialize OpenCV for camera
        self.capture = cv2.VideoCapture(0)
        self.is_camera_on = False
        self.current_image = None

        # Create labels and buttons
        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.pack(pady=20)

        self.start_camera_button = tk.Button(self.root, text="Start Camera", command=self.start_camera)
        self.start_camera_button.pack(pady=10)

        self.capture_button = tk.Button(self.root, text="Capture Photo", command=self.capture_photo, state=tk.DISABLED)
        self.capture_button.pack(pady=10)

        self.view_photos_button = tk.Button(self.root, text="View Photos", command=self.view_photos)
        self.view_photos_button.pack(pady=10)

        self.stop_camera_button = tk.Button(self.root, text="Stop Camera", command=self.stop_camera, state=tk.DISABLED)
        self.stop_camera_button.pack(pady=10)
        
    def start_camera(self):
        self.is_camera_on = True
        self.capture_button.config(state=tk.NORMAL)
        self.stop_camera_button.config(state=tk.NORMAL)
        self.start_camera_button.config(state=tk.DISABLED)
        self.update_frame()

    def stop_camera(self):
        self.is_camera_on = False
        self.capture.release()  # Release the camera
        self.canvas.delete("all")
        self.start_camera_button.config(state=tk.NORMAL)
        self.stop_camera_button.config(state=tk.DISABLED)
        self.capture_button.config(state=tk.DISABLED)

    def update_frame(self):
        if self.is_camera_on:
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.current_image = Image.fromarray(frame)
                self.display_image(self.current_image)
            self.root.after(10, self.update_frame)  # Refresh the frame

    def display_image(self, img):
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)
        self.canvas.image = img_tk

    def capture_photo(self):
        if self.current_image:
            photo_name = f"{self.photos_folder}/photo_{len(os.listdir(self.photos_folder)) + 1}.jpg"
            self.current_image.save(photo_name)
            print(f"Photo saved as {photo_name}")

    def view_photos(self):
        self.view_window = tk.Toplevel(self.root)
        self.view_window.title("View Photos")
        self.view_window.geometry("800x600")

        self.photo_list = os.listdir(self.photos_folder)
        if not self.photo_list:
            tk.Label(self.view_window, text="No photos available!").pack(pady=20)
            return

        # Listbox to select a photo
        self.photo_listbox = tk.Listbox(self.view_window)
        for photo in self.photo_list:
            self.photo_listbox.insert(tk.END, photo)
        self.photo_listbox.pack(pady=20)

        self.select_button = tk.Button(self.view_window, text="Select Photo", command=self.select_photo)
        self.select_button.pack(pady=10)

        # Canvas to display selected photo
        self.canvas_in_view = tk.Canvas(self.view_window, width=800, height=600)
        self.canvas_in_view.pack(pady=20)

    def select_photo(self):
        selected_idx = self.photo_listbox.curselection()
        if selected_idx:
            selected_photo = self.photo_list[selected_idx[0]]
            self.display_selected_photo(selected_photo)

    def display_selected_photo(self, photo_name):
        photo_path = os.path.join(self.photos_folder, photo_name)
        img = Image.open(photo_path)
        img.thumbnail((800, 600))  # Resize to fit window
        img_tk = ImageTk.PhotoImage(img)

        # Clear previous image before displaying new one
        self.canvas_in_view.delete("all")
        
        # Display the selected photo
        self.canvas_in_view.create_image(0, 0, image=img_tk, anchor=tk.NW)
        self.canvas_in_view.image = img_tk

# Run the app
root = tk.Tk()
app = CameraPhotoViewer(root)
root.mainloop()
