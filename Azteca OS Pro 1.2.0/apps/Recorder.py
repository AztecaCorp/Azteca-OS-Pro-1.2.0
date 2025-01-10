import os
import pyaudio
import wave
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

class AudioRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Audio Recorder")
        self.root.geometry("400x200")

        # Folder for saving recordings
        self.recordings_folder = "recordings"
        if not os.path.exists(self.recordings_folder):
            os.makedirs(self.recordings_folder)

        self.is_recording = False
        self.frames = []
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100  # Sample rate (Hz)
        self.chunk_size = 1024  # Size of each audio chunk (buffer)
        self.recording_file = None

        self.create_widgets()

    def create_widgets(self):
        # Start/Stop buttons
        self.record_button = tk.Button(self.root, text="Start Recording", command=self.start_recording, width=20)
        self.record_button.pack(pady=10)

        # Stop recording button
        self.stop_button = tk.Button(self.root, text="Stop Recording", command=self.stop_recording, width=20)
        self.stop_button.pack(pady=10)
        self.stop_button.config(state=tk.DISABLED)

        # Save button
        self.save_button = tk.Button(self.root, text="Save Recording", command=self.save_recording, width=20)
        self.save_button.pack(pady=10)
        self.save_button.config(state=tk.DISABLED)

        # Play button
        self.play_button = tk.Button(self.root, text="Play Recording", command=self.play_recording, width=20)
        self.play_button.pack(pady=10)
        self.play_button.config(state=tk.DISABLED)

        # List of saved recordings
        self.recordings_listbox = tk.Listbox(self.root, width=40, height=5)
        self.recordings_listbox.pack(pady=10)
        self.refresh_recordings_list()

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.frames = []
            self.recording_file = None

            self.record_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

            self.audio_stream = pyaudio.PyAudio().open(format=self.audio_format,
                                                       channels=self.channels,
                                                       rate=self.rate,
                                                       input=True,
                                                       frames_per_buffer=self.chunk_size)

            print("Recording started...")
            self.record_audio()

    def record_audio(self):
        if self.is_recording:
            data = self.audio_stream.read(self.chunk_size)
            self.frames.append(data)
            self.root.after(10, self.record_audio)  # Call this method every 10ms to keep recording

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.audio_stream.stop_stream()
            self.audio_stream.close()

            self.record_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.save_button.config(state=tk.NORMAL)
            self.play_button.config(state=tk.NORMAL)

            print("Recording stopped.")

    def save_recording(self):
        # Save the recording in the 'recordings' folder
        file_name = f"recording_{len(os.listdir(self.recordings_folder)) + 1}.wav"
        file_path = os.path.join(self.recordings_folder, file_name)

        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.audio_format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
        
        messagebox.showinfo("Info", f"Recording saved as {file_path}")
        self.frames = []  # Clear the frames after saving
        self.refresh_recordings_list()

    def play_recording(self):
        selected_recording = self.recordings_listbox.get(tk.ACTIVE)
        if selected_recording:
            file_path = os.path.join(self.recordings_folder, selected_recording)
            with wave.open(file_path, 'rb') as wf:
                pyaudio_instance = pyaudio.PyAudio()
                stream = pyaudio_instance.open(format=pyaudio_instance.get_format_from_width(wf.getsampwidth()),
                                               channels=wf.getnchannels(),
                                               rate=wf.getframerate(),
                                               output=True)
                
                data = wf.readframes(self.chunk_size)
                while data:
                    stream.write(data)
                    data = wf.readframes(self.chunk_size)
                stream.stop_stream()
                stream.close()
                pyaudio_instance.terminate()

        else:
            messagebox.showwarning("Warning", "Please select a recording to play!")

    def refresh_recordings_list(self):
        # Clear the listbox and populate it with the current recordings
        self.recordings_listbox.delete(0, tk.END)
        for recording in os.listdir(self.recordings_folder):
            if recording.endswith(".wav"):
                self.recordings_listbox.insert(tk.END, recording)

# Run the application
root = tk.Tk()
app = AudioRecorder(root)
root.mainloop()
