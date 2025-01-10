import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note App")
        self.root.geometry("500x400")

        # Create a folder to store notes
        self.notes_folder = "notes"
        if not os.path.exists(self.notes_folder):
            os.makedirs(self.notes_folder)

        # Create widgets
        self.text_area = tk.Text(self.root, wrap=tk.WORD, width=50, height=10)
        self.text_area.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Save Note", command=self.save_note)
        self.save_button.pack(pady=5)

        self.view_button = tk.Button(self.root, text="View Notes", command=self.view_notes)
        self.view_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Note", command=self.delete_note)
        self.delete_button.pack(pady=5)

        self.notes_listbox = None

    def save_note(self):
        # Get the text from the Text widget
        note_content = self.text_area.get("1.0", tk.END).strip()
        if note_content:
            # Create a new note file
            note_name = f"{len(os.listdir(self.notes_folder)) + 1}.txt"
            note_path = os.path.join(self.notes_folder, note_name)
            
            with open(note_path, "w") as note_file:
                note_file.write(note_content)
            
            # Clear the text area
            self.text_area.delete("1.0", tk.END)
            messagebox.showinfo("Note Saved", "Your note has been saved successfully!")
        else:
            messagebox.showwarning("No Content", "Please write something before saving.")

    def view_notes(self):
        # Create a new window to view notes
        self.view_window = tk.Toplevel(self.root)
        self.view_window.title("View Notes")
        self.view_window.geometry("400x400")

        # Listbox to display saved notes
        self.notes_listbox = tk.Listbox(self.view_window, width=50, height=15)
        self.notes_listbox.pack(pady=10)

        # Populate the Listbox with note filenames
        for note in os.listdir(self.notes_folder):
            self.notes_listbox.insert(tk.END, note)

        # Button to open the selected note
        self.open_button = tk.Button(self.view_window, text="Open Note", command=self.open_note)
        self.open_button.pack(pady=5)

        # Button to delete the selected note
        self.delete_button_in_view = tk.Button(self.view_window, text="Delete Note", command=self.delete_note_in_view)
        self.delete_button_in_view.pack(pady=5)

    def open_note(self):
        # Get the selected note from the listbox
        selected_note = self.notes_listbox.curselection()
        if selected_note:
            note_name = self.notes_listbox.get(selected_note[0])
            note_path = os.path.join(self.notes_folder, note_name)
            
            # Open the note and display its content in the text area
            with open(note_path, "r") as note_file:
                note_content = note_file.read()
            
            self.view_note_window = tk.Toplevel(self.root)
            self.view_note_window.title("View Note")
            self.view_note_window.geometry("400x400")

            # Create a Text widget to show the note content
            text_area = tk.Text(self.view_note_window, wrap=tk.WORD, width=50, height=10)
            text_area.pack(pady=10)
            text_area.insert(tk.END, note_content)
            text_area.config(state=tk.DISABLED)  # Make the text area read-only
        else:
            messagebox.showwarning("No Selection", "Please select a note to open.")

    def delete_note(self):
        # Get the text from the Text widget
        note_content = self.text_area.get("1.0", tk.END).strip()
        if note_content:
            # Create a new note file
            note_name = f"{len(os.listdir(self.notes_folder)) + 1}.txt"
            note_path = os.path.join(self.notes_folder, note_name)
            
            with open(note_path, "w") as note_file:
                note_file.write(note_content)
            
            # Clear the text area
            self.text_area.delete("1.0", tk.END)
            messagebox.showinfo("Note Saved", "Your note has been saved successfully!")
        else:
            messagebox.showwarning("No Content", "Please write something before saving.")

    def delete_note_in_view(self):
        # Delete the selected note from the listbox
        selected_note = self.notes_listbox.curselection()
        if selected_note:
            note_name = self.notes_listbox.get(selected_note[0])
            note_path = os.path.join(self.notes_folder, note_name)
            
            # Delete the selected note file
            os.remove(note_path)
            self.notes_listbox.delete(selected_note)
            messagebox.showinfo("Note Deleted", "The selected note has been deleted successfully!")
        else:
            messagebox.showwarning("No Selection", "Please select a note to delete.")

# Create the main window and run the app
root = tk.Tk()
note_app = NoteApp(root)
root.mainloop()
