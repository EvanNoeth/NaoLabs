import sys, time, os, qi, threading
import tkinter as tk
from tkinter import ttk, messagebox

#Address: 10.117.35.237

def main():
    root = tk.Tk()
    root.title("NAO 3 Good Things Panel")
    root.geometry("500x450")

    state = {
        "session": None,
        "tts": None,
        "posture": None,
        "behavior": None,
        "joint": None,
    }

    def run_async(func, *args):
        if not state["session"]:
            messagebox.showwarning("Not Connected", "Please connect to the robot first.")
            return
        threading.Thread(target=func, args=args, daemon=True).start()

    def say(text):
        if text.strip() and state["tts"]:
            state["tts"].say(str(text))

    def go_to_posture(posture_name):
        if state["posture"]:
            state["posture"].goToPosture(posture_name, 1.0)

    def stop_all():
        if state["joint"]:
            state["joint"].rest()

    def connect_robot():
        ip = ip_entry.get()
        port = "9559"

        state["session"] = qi.Session()

        try:
            state["session"].connect(f"tcp://{ip}:{port}")
            state["tts"] = state["session"].service("ALTextToSpeech")
            state["posture"] = state["session"].service("ALRobotPosture")
            state["joint"] = state["session"].service("ALMotion")

            messagebox.showinfo("Success", f"Successfully connected to robot at {ip}!")
            btn_connect.config(text="Connected", state="disabled")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to {ip}:\n{e}")

    # connection ui
    conn_frame = ttk.LabelFrame(root, text=" Robot Connection ", padding=10)
    conn_frame.pack(fill="x", padx=10, pady=10)

    ttk.Label(conn_frame, text="Robot IP:").grid(row=0, column=0, padx=5, sticky="w")
    ip_entry = ttk.Entry(conn_frame)
    ip_entry.insert(0, "10.117.35.237")
    ip_entry.grid(row=0, column=1, padx=5, sticky="ew")

    btn_connect = ttk.Button(conn_frame, text="Connect", command=connect_robot)
    btn_connect.grid(row=0, column=2, padx=5)

    # control ui
    control_notebook = ttk.Notebook(root)
    control_notebook.pack(fill="both", expand=True, padx=10, pady=10)

    tab_speech = ttk.Frame(control_notebook, padding=10)
    control_notebook.add(tab_speech, text="Speech Controls")

    # script
    ttk.Label(tab_speech, text="Quick Phrases:", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
    phrases = [
        ("Intro", "Hello, I am Nao. Do you want to play the three good things exercise with me? Let's go back and fourth sharing three good things that happened to us this week!"),
        ("1st Good Thing", "I was happy to have no exams this week. Alright, how about you?"),
        ("2nd Good Thing", "I'm grateful that my robot parents came to campus to visit me! Your turn!"),
        ("3rd Good Thing", "I'm psyched that I got to go to a college football game! How about your last thing?")
    ]

    btn_frame = ttk.Frame(tab_speech)
    btn_frame.pack(fill="x", pady=5)
    for label, text in phrases:
        btn = ttk.Button(btn_frame, text=label, command=lambda t=text: run_async(say, t))
        btn.pack(side="left", padx=2, pady=2, fill="x", expand=True)

    ttk.Label(tab_speech, text="Custom Speech Entry:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(15, 5))
    speech_entry = ttk.Entry(tab_speech)
    speech_entry.pack(fill="x", pady=2)

    btn_say_custom = ttk.Button(tab_speech, text="Speak Custom Text",
                                command=lambda: run_async(say, speech_entry.get()))
    btn_say_custom.pack(anchor="e", pady=5)

    tab_motion = ttk.Frame(control_notebook, padding=10)
    control_notebook.add(tab_motion, text="Motion and Postures")

    ttk.Label(tab_motion, text="Change Base Postures:", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
    postures = ["Stand", "LyingBack", "Sit", "SitRelax"]

    for pos in postures:
        btn = ttk.Button(tab_motion, text=pos, command=lambda p=pos: run_async(go_to_posture, p))
        btn.pack(fill="x", pady=2)

    btn_stop = tk.Button(root, text="RELAX (SPARE JOINTS)",
                         bg="red", fg="white", font=("Arial", 11, "bold"),
                         command=lambda: run_async(stop_all))
    btn_stop.pack(fill="x", padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()