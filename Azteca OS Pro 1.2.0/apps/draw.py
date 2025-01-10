import tkinter as tk
from tkinter import filedialog, simpledialog, colorchooser
from PIL import Image, ImageDraw
import os
from datetime import datetime

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Drawing App")

        # Initializing drawing settings
        self.color = "black"
        self.brush_size = 5
        self.last_x, self.last_y = None, None

        # Creating the canvas
        self.canvas = tk.Canvas(self.root, bg="white", width=600, height=400)
        self.canvas.pack(padx=10, pady=10)

        # Creating buttons for features
        self.create_buttons()

        # Create an image to draw on
        self.image = Image.new("RGB", (600, 400), color="white")
        self.draw = ImageDraw.Draw(self.image)

        # Binding mouse events for drawing
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        # Make sure the drawings folder exists
        self.drawings_folder = "drawings"
        if not os.path.exists(self.drawings_folder):
            os.makedirs(self.drawings_folder)

    def create_buttons(self):
        """Create buttons for color change, brush size, clear and save."""
        # Color button
        color_button = tk.Button(self.root, text="Color", command=self.change_color, width=10)
        color_button.pack(side=tk.LEFT, padx=5)

        # Brush size button
        size_button = tk.Button(self.root, text="Brush Size", command=self.change_brush_size, width=10)
        size_button.pack(side=tk.LEFT, padx=5)

        # Clear canvas button
        clear_button = tk.Button(self.root, text="Clear", command=self.clear_canvas, width=10)
        clear_button.pack(side=tk.LEFT, padx=5)

        # Save button
        save_button = tk.Button(self.root, text="Save", command=self.save_canvas, width=10)
        save_button.pack(side=tk.LEFT, padx=5)

    def paint(self, event):
        """Draw on the canvas."""
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill=self.color, capstyle=tk.ROUND, smooth=True)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.color, width=self.brush_size)
        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """Reset the last position after the mouse button is released."""
        self.last_x = None
        self.last_y = None

    def change_color(self):
        """Open a color picker to choose a color."""
        color = colorchooser.askcolor()[1]
        if color:
            self.color = color

    def change_brush_size(self):
        """Change the brush size."""
        size = simpledialog.askinteger("Brush Size", "Enter brush size (1-10):", minvalue=1, maxvalue=10)
        if size:
            self.brush_size = size

    def clear_canvas(self):
        """Clear the entire canvas."""
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), color="white")
        self.draw = ImageDraw.Draw(self.image)

    def save_canvas(self):
        """Save the canvas as a PNG image in the 'drawings' folder."""
        # Generate a unique filename based on the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(self.drawings_folder, f"drawing_{timestamp}.png")
        
        # Save the image in the drawings folder
        self.image.save(file_path, format="PNG")
        print(f"Saved drawing as {file_path}")

# Main application window
root = tk.Tk()
app = DrawingApp(root)
root.mainloop()
