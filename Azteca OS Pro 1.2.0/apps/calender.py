import tkinter as tk
from tkinter import messagebox, simpledialog
import calendar
from datetime import datetime

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar App")

        self.year = 2024
        self.month = 12
        self.events = {}  # Dictionary to store events in the format { 'YYYY-MM-DD': ['event1', 'event2'] }

        self.load_events()  # Load events from the file
        # Create UI components
        self.create_widgets()
        self.display_calendar()

    def create_widgets(self):
        """Create widgets for navigation and display."""
        # Frame for the calendar
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack(pady=20)

        # Year and Month Navigation
        self.nav_frame = tk.Frame(self.root)
        self.nav_frame.pack(pady=10)

        # Previous and Next Month Buttons
        self.prev_button = tk.Button(self.nav_frame, text="< Prev", command=self.prev_month)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.month_label = tk.Label(self.nav_frame, text="", width=20)
        self.month_label.grid(row=0, column=1)

        self.next_button = tk.Button(self.nav_frame, text="Next >", command=self.next_month)
        self.next_button.grid(row=0, column=2, padx=5)

        # Event Button (Optional)
        self.event_button = tk.Button(self.nav_frame, text="Add Event", command=self.add_event)
        self.event_button.grid(row=1, column=1, pady=5)

    def display_calendar(self):
        """Display the calendar for the current month and year."""
        # Get the calendar for the current month and year
        cal = calendar.monthcalendar(self.year, self.month)

        # Update the month label
        month_name = calendar.month_name[self.month]
        self.month_label.config(text=f"{month_name} {self.year}")

        # Clear any previous calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Create day headers
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day_name in enumerate(day_names):
            tk.Label(self.calendar_frame, text=day_name, width=10, height=2, relief="solid").grid(row=0, column=col)

        # Create calendar grid
        for row, week in enumerate(cal, start=1):
            for col, day in enumerate(week):
                if day != 0:
                    date_str = f"{self.year}-{self.month:02d}-{day:02d}"
                    button = tk.Button(self.calendar_frame, text=str(day), width=10, height=2,
                                       command=lambda day=day: self.select_day(day))
                    button.grid(row=row, column=col)

                    # Highlight current day if it matches
                    today = datetime.today()
                    if today.year == self.year and today.month == self.month and today.day == day:
                        button.config(bg="yellow")

    def prev_month(self):
        """Go to the previous month."""
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.display_calendar()

    def next_month(self):
        """Go to the next month."""
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.display_calendar()

    def select_day(self, day):
        """Handle day selection and display events."""
        day_str = f"{self.year}-{self.month:02d}-{day:02d}"
        events = self.events.get(day_str, [])
        
        event_info = "\n".join(events) if events else "No events for this day."
        
        # Display events for the selected day
        messagebox.showinfo(f"Events for {calendar.month_name[self.month]} {day}, {self.year}",
                            event_info)

    def add_event(self):
        """Allow user to add an event to the selected date."""
        day = simpledialog.askinteger("Add Event", "Enter the day for the event (1-31):", minvalue=1, maxvalue=31)
        if day:
            event = simpledialog.askstring("Event", f"Enter the event for {calendar.month_name[self.month]} {day}, {self.year}:")
            if event:
                day_str = f"{self.year}-{self.month:02d}-{day:02d}"
                if day_str not in self.events:
                    self.events[day_str] = []
                self.events[day_str].append(event)
                self.save_events()  # Save the events to file
                messagebox.showinfo("Event Added", f"Event '{event}' added for {calendar.month_name[self.month]} {day}, {self.year}")
            else:
                messagebox.showwarning("No Event", "No event entered.")
        else:
            messagebox.showwarning("Invalid Day", "Invalid day entered.")

    def load_events(self):
        """Load events from the events.txt file."""
        try:
            with open("events.txt", "r") as file:
                for line in file:
                    date_str, events_str = line.strip().split(": ")
                    events_list = events_str.split(", ")
                    self.events[date_str] = events_list
        except FileNotFoundError:
            # If the file doesn't exist, just continue with an empty event list
            pass

    def save_events(self):
        """Save events to the events.txt file."""
        with open("events.txt", "w") as file:
            for date_str, events_list in self.events.items():
                events_str = ", ".join(events_list)
                file.write(f"{date_str}: {events_str}\n")

# Main application window
root = tk.Tk()
app = CalendarApp(root)
root.mainloop()
