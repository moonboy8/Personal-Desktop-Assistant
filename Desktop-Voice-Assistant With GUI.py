import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import os
import random
import pyjokes
import threading

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Functions
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    update_text_box(f"Jarvis: {audio}")

def time():
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak(f"The current time is {current_time}")

def date():
    now = datetime.datetime.now()
    speak(f"The current date is {now.day} {now.strftime('%B')} {now.year}")

def wishme():
    hour = datetime.datetime.now().hour
    greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
    speak(f"{greeting}, sir. Jarvis at your service. How can I assist you today?")

def takecommand():
    """Takes microphone input from the user and returns it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        update_text_box("Listening...")
        progress_bar.start()  # Start the progress bar
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)
            query = r.recognize_google(audio, language="en-in")
            update_text_box(f"You: {query}")
            progress_bar.stop()  # Stop the progress bar once recognition is done
            return query.lower()
        except Exception as e:
            update_text_box("Error: Unable to recognize speech")
            progress_bar.stop()  # Stop the progress bar on error
            return None

def play_music():
    music_dir = os.path.expanduser("~\\Music")
    songs = os.listdir(music_dir)
    if songs:
        song = random.choice(songs)
        os.startfile(os.path.join(music_dir, song))
        speak(f"Playing {song}")
    else:
        speak("No music files found.")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def help_menu():
    """Displays the help menu."""
    help_text = (
        "Welcome to Jarvis Voice Assistant!\n\n"
        "Commands you can try:\n"
        "- Say 'time' to get the current time.\n"
        "- Say 'date' to know today's date.\n"
        "- Say 'play music' to play a random song from your Music folder.\n"
        "- Say 'tell me a joke' for a fun joke.\n"
        "- Use the buttons for manual control.\n"
        "- Speak 'exit' to close the application."
    )
    messagebox.showinfo("Help", help_text)

def update_text_box(text):
    """Updates the text box with new text."""
    text_box.configure(state="normal")
    text_box.insert("end", text + "\n")
    text_box.configure(state="disabled")
    text_box.see("end")

def listen_for_commands():
    """Runs speech recognition in a separate thread."""
    while True:
        query = takecommand()
        if query:
            if "time" in query:
                time()
            elif "date" in query:
                date()
            elif "play music" in query:
                play_music()
            elif "tell me a joke" in query:
                tell_joke()
            elif "exit" in query:
                speak("Exiting. Goodbye!")
                root.quit()
                break

# GUI Setup
ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

root = ctk.CTk()
root.title("Jarvis Voice Assistant")
root.geometry("1000x700")

# Header
header_frame = ctk.CTkFrame(root, corner_radius=15)
header_frame.pack(fill="x", padx=20, pady=10)

header_label = ctk.CTkLabel(
    header_frame, text="Jarvis Voice Assistant", font=("Helvetica", 30, "bold")
)
header_label.pack(pady=10)

# Main Frame
main_frame = ctk.CTkFrame(root, corner_radius=15)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Sidebar for Buttons
button_frame = ctk.CTkFrame(main_frame, width=200, corner_radius=15)
button_frame.pack(side="left", fill="y", padx=10, pady=10)

buttons = [
    ("Time", time),
    ("Date", date),
    ("Play Music", play_music),
    ("Tell Me a Joke", tell_joke),
    ("Help", help_menu),
    ("Exit", root.destroy),
]

for label, command in buttons:
    btn = ctk.CTkButton(
        button_frame,
        text=label,
        command=command,
        width=160,
        height=40,
        font=("Arial", 14, "bold"),
    )
    btn.pack(pady=10)

# Chat Display
chat_frame = ctk.CTkFrame(main_frame, corner_radius=15)
chat_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

text_box = ctk.CTkTextbox(
    chat_frame,
    font=("Courier", 14),
    state="disabled",
    wrap="word",
    width=700,
    height=400,
)
text_box.pack(fill="both", expand=True, padx=10, pady=10)

# Progress Bar for Listening
progress_bar = Progressbar(root, length=200, mode="indeterminate", maximum=100)
progress_bar.pack(pady=10)

# Footer
footer_label = ctk.CTkLabel(
    root, text="Developed by [Shrivardhan Boini] © 2024", font=("Helvetica", 12)
)
footer_label.pack(side="bottom", pady=5)

# Start the Assistant
wishme()

# Start the speech recognition in a separate thread
recognition_thread = threading.Thread(target=listen_for_commands, daemon=True)
recognition_thread.start()

# Run the GUI
root.mainloop()
