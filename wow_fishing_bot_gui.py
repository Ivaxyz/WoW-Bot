import tkinter as tk
from tkinter import ttk, filedialog
import json
import threading
import time
from wow_fishing_bot import cast_fishing, find_bobber, detect_bite, click_bobber, loot
from PIL import Image, ImageTk

class FishingBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WoW Fishing Bot")
        self.root.geometry("400x300")
        
        # Bot-Status
        self.is_running = False
        self.bot_thread = None
        
        # Konfiguration laden
        self.load_config()
        
        # Logo laden und anzeigen
        logo_image = Image.open("logo.png")
        logo_image = logo_image.resize((120, 120), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = ttk.Label(self.root, image=self.logo_photo)
        logo_label.pack(pady=(10, 0))
        
        # GUI-Elemente erstellen
        self.create_widgets()
        
    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {
                "template_path": "bobber_template.png",
                "bobber_threshold": 0.4,
                "bite_threshold": 15,
                "scan_region_size": 60
            }
            self.save_config()
    
    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def create_widgets(self):
        # Logo laden und anzeigen
        logo_image = Image.open("logo.png")
        logo_image = logo_image.resize((120, 120), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = ttk.Label(self.root, image=self.logo_photo)
        logo_label.pack(pady=(10, 0))
        
        # Template-Auswahl
        template_frame = ttk.LabelFrame(self.root, text="Bobber Template", padding=10)
        template_frame.pack(fill="x", padx=10, pady=5)
        
        self.template_path_var = tk.StringVar(value=self.config["template_path"])
        template_entry = ttk.Entry(template_frame, textvariable=self.template_path_var, width=30)
        template_entry.pack(side="left", padx=5)
        
        template_button = ttk.Button(template_frame, text="Auswählen", command=self.select_template)
        template_button.pack(side="left", padx=5)
        
        # Bobber Threshold
        bobber_frame = ttk.LabelFrame(self.root, text="Bobber Erkennung (0.0 - 1.0)", padding=10)
        bobber_frame.pack(fill="x", padx=10, pady=5)
        
        self.bobber_threshold_var = tk.DoubleVar(value=self.config["bobber_threshold"])
        bobber_scale = ttk.Scale(bobber_frame, from_=0.0, to=1.0, 
                                variable=self.bobber_threshold_var,
                                orient="horizontal", length=300)
        bobber_scale.pack(fill="x")
        
        bobber_label = ttk.Label(bobber_frame, textvariable=self.bobber_threshold_var)
        bobber_label.pack()
        
        # Bite Threshold
        bite_frame = ttk.LabelFrame(self.root, text="Biss Erkennung (0 - 50)", padding=10)
        bite_frame.pack(fill="x", padx=10, pady=5)
        
        self.bite_threshold_var = tk.IntVar(value=self.config["bite_threshold"])
        bite_scale = ttk.Scale(bite_frame, from_=0, to=50,
                              variable=self.bite_threshold_var,
                              orient="horizontal", length=300)
        bite_scale.pack(fill="x")
        
        bite_label = ttk.Label(bite_frame, textvariable=self.bite_threshold_var)
        bite_label.pack()
        
        # Scan Region Size
        scan_frame = ttk.LabelFrame(self.root, text="Scan-Bereich (20 - 200 Pixel)", padding=10)
        scan_frame.pack(fill="x", padx=10, pady=5)
        
        self.scan_region_var = tk.IntVar(value=self.config.get("scan_region_size", 60))
        scan_scale = ttk.Scale(scan_frame, from_=20, to=200,
                              variable=self.scan_region_var,
                              orient="horizontal", length=300)
        scan_scale.pack(fill="x")
        
        scan_label = ttk.Label(scan_frame, textvariable=self.scan_region_var)
        scan_label.pack()
        
        # Start/Stop Button
        self.start_stop_button = ttk.Button(self.root, text="Start", command=self.toggle_bot)
        self.start_stop_button.pack(side="bottom", padx=10, pady=10)
        
    def select_template(self):
        filename = filedialog.askopenfilename(
            title="Bobber Template auswählen",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            self.template_path_var.set(filename)
            self.config["template_path"] = filename
            self.save_config()
    
    def toggle_bot(self):
        if not self.is_running:
            self.start_bot()
        else:
            self.stop_bot()
    
    def start_bot(self):
        self.is_running = True
        self.start_stop_button.config(text="Stop")
        self.bot_thread = threading.Thread(target=self.bot_loop)
        self.bot_thread.start()
    
    def stop_bot(self):
        self.is_running = False
        self.start_stop_button.config(text="Start")
        if self.bot_thread:
            self.bot_thread.join()
    
    def bot_loop(self):
        while self.is_running:
            # Konfiguration aktualisieren
            self.config["bobber_threshold"] = self.bobber_threshold_var.get()
            self.config["bite_threshold"] = self.bite_threshold_var.get()
            self.config["scan_region_size"] = self.scan_region_var.get()
            self.save_config()
            
            # Bot-Logik
            cast_fishing()
            time.sleep(1.5)
            
            bobber_pos = find_bobber()
            if bobber_pos:
                if detect_bite(bobber_pos):
                    click_bobber(bobber_pos)
                    time.sleep(1.0)
                    loot()
            time.sleep(2.0)

if __name__ == "__main__":
    root = tk.Tk()
    app = FishingBotGUI(root)
    root.mainloop() 