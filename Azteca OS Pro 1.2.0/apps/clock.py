import tkinter as tk
from time import strftime

class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clock App")

        # Set the clock display style
        self.clock_label = tk.Label(self.root, font=("calibri", 50, "bold"), background="black", foreground="yellow")
        self.clock_label.pack(anchor="center")

        # Call the method to update the time
        self.update_time()

    def update_time(self):
        """Update the time every second."""
        time_string = strftime('%I:%M:%S %p')  # 12-hour format with AM/PM
        # You can change the format to 24-hour by using '%H:%M:%S'
        self.clock_label.config(text=time_string)
        
        # Call the update_time method every 1000 milliseconds (1 second)
        self.root.after(1000, self.update_time)

# Create the main window
root = tk.Tk()
clock_app = ClockApp(root)

# Run the Tkinter event loop
root.mainloop()
