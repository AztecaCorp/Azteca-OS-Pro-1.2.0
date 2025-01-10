import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
import pygame

class MusicPlayerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Music Player")
        self.root.geometry("400x300")
        self.music_dir = "music"
        self.playlist = []
        self.current_index = 0
        self.is_playing = False

        # Initialize pygame mixer
        pygame.mixer.init()

        # Create UI components
        self.create_widgets()

        # Ensure music directory exists and load playlist
        if not os.path.exists(self.music_dir):
            os.makedirs(self.music_dir)
        self.load_playlist()

    def create_widgets(self):
        # Playlist display
        self.playlist_box = Listbox(self.root, selectmode=tk.SINGLE, bg="white", fg="black", width=50, height=10)
        self.playlist_box.pack(pady=10)

        # Control buttons
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack()

        self.play_button = tk.Button(self.controls_frame, text="Play", command=self.play)
        self.play_button.grid(row=0, column=0, padx=5)

        self.pause_button = tk.Button(self.controls_frame, text="Pause", command=self.pause)
        self.pause_button.grid(row=0, column=1, padx=5)

        self.resume_button = tk.Button(self.controls_frame, text="Resume", command=self.resume)
        self.resume_button.grid(row=0, column=2, padx=5)

        self.stop_button = tk.Button(self.controls_frame, text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=3, padx=5)

        self.add_button = tk.Button(self.controls_frame, text="Add Song", command=self.add_song)
        self.add_button.grid(row=1, column=2, padx=5, pady=5)

        self.exit_button = tk.Button(self.controls_frame, text="Exit", command=self.root.quit)
        self.exit_button.grid(row=1, column=3, padx=5, pady=5)

    def load_playlist(self):
        self.playlist = [f for f in os.listdir(self.music_dir) if f.endswith(('.mp3', '.wav'))]
        self.playlist_box.delete(0, tk.END)
        for song in self.playlist:
            self.playlist_box.insert(tk.END, song)

    def play(self):
        if not self.playlist:
            messagebox.showinfo("Info", "No songs in the playlist!")
            return

        selected = self.playlist_box.curselection()
        if selected:
            self.current_index = selected[0]

        song = self.playlist[self.current_index]
        song_path = os.path.join(self.music_dir, song)
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        self.is_playing = True
        messagebox.showinfo("Playing", f"Now playing: {song}")

    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False

    def resume(self):
        if not self.is_playing:
            pygame.mixer.music.unpause()
            self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play()

    def previous(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play()

    def add_song(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(self.music_dir, file_name)
            if not os.path.exists(dest_path):
                os.rename(file_path, dest_path)
                self.load_playlist()
                messagebox.showinfo("Success", f"Added {file_name} to playlist.")
            else:
                messagebox.showwarning("Warning", "Song already exists in the playlist!")

# Run the application
root = tk.Tk()
app = MusicPlayerGUI(root)
root.mainloop()
