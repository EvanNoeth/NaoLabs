import sys, time, os, qi, threading
import tkinter as tk
from tkinter import ttk, messagebox

#Address: 10.117.35.237
class NaoWizardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NAO 3 Good Things Panel")
        self.root.geometry("500x450")
        
        self.session = None
        self.tts = None
        self.posture = None
        self.behavior = None
        self.joint = None
        
        self.create_connection_ui()
        self.create_control_ui()

    def create_connection_ui(self):
        conn_frame = ttk.LabelFrame(self.root, text=" Robot Connection ", padding=10)
        conn_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(conn_frame, text="Robot IP:").grid(row=0, column=0, padx=5, sticky="w")
        self.ip_entry = ttk.Entry(conn_frame)
        self.ip_entry.insert(0, "10.117.35.237")
        self.ip_entry.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.btn_connect = ttk.Button(conn_frame, text="Connect", command=self.connect_robot)
        self.btn_connect.grid(row=0, column=2, padx=5)

    def create_control_ui(self):
        self.control_notebook = ttk.Notebook(self.root)
        self.control_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        tab_speech = ttk.Frame(self.control_notebook, padding=10)
        self.control_notebook.add(tab_speech, text="Speech Controls")
        
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
            btn = ttk.Button(btn_frame, text=label, command=lambda t=text: self.run_async(self.say, t))
            btn.pack(side="left", padx=2, pady=2, fill="x", expand=True)
            
        ttk.Label(tab_speech, text="Custom Speech Entry:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(15, 5))
        self.speech_entry = ttk.Entry(tab_speech)
        self.speech_entry.pack(fill="x", pady=2)
        
        btn_say_custom = ttk.Button(tab_speech, text="Speak Custom Text", 
                                    command=lambda: self.run_async(self.say, self.speech_entry.get()))
        btn_say_custom.pack(anchor="e", pady=5)

        tab_motion = ttk.Frame(self.control_notebook, padding=10)
        self.control_notebook.add(tab_motion, text="Motion and Postures")
        
        ttk.Label(tab_motion, text="Change Base Postures:", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
        postures = ["Stand", "LyingBack", "Sit", "SitRelax"]
        
        for pos in postures:
            btn = ttk.Button(tab_motion, text=pos, command=lambda p=pos: self.run_async(self.go_to_posture, p))
            btn.pack(fill="x", pady=2)
        
        self.btn_stop = tk.Button(self.root, text="RELAX (SPARE JOINTS)", 
                                  bg="red", fg="white", font=("Arial", 11, "bold"),
                                  command=lambda: self.run_async(self.stop_all))
        self.btn_stop.pack(fill="x", padx=10, pady=10)

    def run_async(self, func, *args):
        if not self.session:
            messagebox.showwarning("Not Connected", "Please connect to the robot first.")
            return
        threading.Thread(target=func, args=args, daemon=True).start()

    def say(self, text):
        if text.strip() and self.tts:
            self.tts.say(str(text))

    def go_to_posture(self, posture_name):
        if self.posture:
            self.posture.goToPosture(posture_name, 1.0)

    def stop_all(self):
        if self.joint:
            self.joint.rest()



    def connect_robot(self):
        ip = self.ip_entry.get()
        port = "9559"
        
        self.session = qi.Session()

        try:
            self.session.connect(f"tcp://{ip}:{port}")
            self.tts = self.session.service("ALTextToSpeech")
            self.posture = self.session.service("ALRobotPosture")
            self.joint = self.session.service("ALMotion")
            
            messagebox.showinfo("Success", f"Successfully connected to robot at {ip}!")
            self.btn_connect.config(text="Connected", state="disabled")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to {ip}:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NaoWizardApp(root)
    root.mainloop()
