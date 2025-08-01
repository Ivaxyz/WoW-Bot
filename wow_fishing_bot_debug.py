import time
import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import json
import logging
import sys
import os
import subprocess
import platform

# === LOGGING SETUP ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# === DIAGNOSE FUNKTIONEN ===
def diagnose_system():
    """Führt eine umfassende Systemdiagnose durch."""
    logging.info("=== SYSTEMDIAGNOSE START ===")
    
    # Betriebssystem
    logging.info(f"Betriebssystem: {platform.system()} {platform.release()}")
    
    # Python-Version
    logging.info(f"Python-Version: {sys.version}")
    
    # Abhängigkeiten prüfen
    if not check_dependencies():
        return False
    
    # Dateien prüfen
    if not check_files():
        return False
    
    # WoW-Fenster prüfen
    if not check_wow_window():
        return False
    
    # Berechtigungen prüfen
    if not check_permissions():
        return False
    
    # Test der Tastatureingaben
    if not test_keyboard_input():
        return False
    
    logging.info("=== SYSTEMDIAGNOSE ERFOLGREICH ===")
    return True

def check_wow_window():
    """Prüft ob WoW läuft und im Vordergrund ist."""
    try:
        # Suche nach WoW-Fenstern
        wow_windows = []
        for window in pyautogui.getAllWindows():
            if 'world of warcraft' in window.title.lower() or 'wow' in window.title.lower():
                wow_windows.append(window)
        
        if not wow_windows:
            logging.error("❌ Kein WoW-Fenster gefunden!")
            logging.error("Stelle sicher, dass World of Warcraft läuft.")
            return False
        
        logging.info(f"✓ {len(wow_windows)} WoW-Fenster gefunden")
        
        # Prüfe ob WoW im Vordergrund ist
        active_window = pyautogui.getActiveWindow()
        if active_window and any(wow.title == active_window.title for wow in wow_windows):
            logging.info("✓ WoW ist im Vordergrund")
        else:
            logging.warning("⚠️ WoW ist NICHT im Vordergrund")
            logging.info("Versuche WoW in den Vordergrund zu bringen...")
            try:
                wow_windows[0].activate()
                time.sleep(1)
                logging.info("✓ WoW in den Vordergrund gebracht")
            except Exception as e:
                logging.error(f"❌ Konnte WoW nicht in den Vordergrund bringen: {e}")
                return False
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Fehler beim Prüfen des WoW-Fensters: {e}")
        return False

def check_permissions():
    """Prüft Berechtigungen für Tastatur- und Mauszugriff."""
    try:
        # Teste ob pyautogui funktioniert
        current_pos = pyautogui.position()
        logging.info(f"✓ Mausposition abrufbar: {current_pos}")
        
        # Teste ob Screenshots möglich sind
        screenshot = ImageGrab.grab()
        logging.info(f"✓ Screenshots möglich: {screenshot.size}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Berechtigungsproblem: {e}")
        logging.error("Versuche den Bot als Administrator auszuführen")
        return False

def test_keyboard_input():
    """Testet ob Tastatureingaben funktionieren."""
    try:
        logging.info("Teste Tastatureingaben...")
        logging.info("Drücke '1' in 3 Sekunden - stelle sicher, dass WoW aktiv ist!")
        
        for i in range(3, 0, -1):
            logging.info(f"Test in {i} Sekunden...")
            time.sleep(1)
        
        logging.info("Drücke Test-Taste '1'")
        pyautogui.press('1')
        logging.info("✓ Tastatureingabe erfolgreich")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Tastatureingabe fehlgeschlagen: {e}")
        return False

def install_missing_packages():
    """Installiert fehlende Python-Pakete."""
    missing_packages = []
    
    try:
        import pyautogui
    except ImportError:
        missing_packages.append('pyautogui')
    
    try:
        import cv2
    except ImportError:
        missing_packages.append('opencv-python')
    
    try:
        import numpy
    except ImportError:
        missing_packages.append('numpy')
    
    try:
        from PIL import ImageGrab
    except ImportError:
        missing_packages.append('pillow')
    
    if missing_packages:
        logging.info(f"Installiere fehlende Pakete: {missing_packages}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            logging.info("✓ Pakete erfolgreich installiert")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Fehler beim Installieren der Pakete: {e}")
            return False
    
    return True

# === KONFIGURATION ===
def load_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            logging.info(f"Konfiguration geladen: {config}")
            return config
    except FileNotFoundError:
        logging.warning("config.json nicht gefunden, erstelle Standard-Konfiguration")
        config = {
            "template_path": "bobber_template.png",
            "bobber_threshold": 0.4,
            "bite_threshold": 15,
            "scan_region_size": 60
        }
        # Erstelle config.json
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        logging.info("✓ config.json erstellt")
        return config
    except json.JSONDecodeError as e:
        logging.error(f"Fehler beim Lesen der config.json: {e}")
        return {
            "template_path": "bobber_template.png",
            "bobber_threshold": 0.4,
            "bite_threshold": 15,
            "scan_region_size": 60
        }

def check_dependencies():
    """Überprüft ob alle erforderlichen Pakete installiert sind."""
    required_packages = ['pyautogui', 'cv2', 'numpy', 'PIL']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'PIL':
                from PIL import ImageGrab
            else:
                __import__(package)
            logging.info(f"✓ {package} ist installiert")
        except ImportError:
            missing_packages.append(package)
            logging.error(f"✗ {package} ist NICHT installiert")
    
    if missing_packages:
        logging.error(f"Fehlende Pakete: {missing_packages}")
        logging.info("Versuche automatische Installation...")
        if not install_missing_packages():
            logging.error("Installieren Sie sie manuell mit: pip install " + " ".join(missing_packages))
            return False
    return True

def check_files():
    """Überprüft ob alle erforderlichen Dateien vorhanden sind."""
    required_files = ['bobber_template.png']
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            logging.info(f"✓ {file} gefunden")
        else:
            missing_files.append(file)
            logging.error(f"✗ {file} NICHT gefunden")
    
    if missing_files:
        logging.error(f"Fehlende Dateien: {missing_files}")
        logging.error("Erstelle Template-Datei...")
        create_template_file()
        return False
    return True

def create_template_file():
    """Erstellt eine einfache Template-Datei für Tests."""
    try:
        # Erstelle ein einfaches Test-Template
        from PIL import Image, ImageDraw
        
        # Erstelle ein 20x20 Pixel großes weißes Bild mit schwarzem Rand
        img = Image.new('RGB', (20, 20), color='white')
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 19, 19], outline='black', width=1)
        
        img.save('bobber_template.png')
        logging.info("✓ Test-Template erstellt (bobber_template.png)")
        logging.warning("⚠️ Verwende das echte Bobber-Template für bessere Erkennung!")
        
    except Exception as e:
        logging.error(f"❌ Konnte Template nicht erstellen: {e}")

config = load_config()
FISHING_KEY = '1'  # Hotkey zum Angeln
LOOT_KEY = 'shift'  # Shift für Auto-Loot (ggf. anpassen)
BOBBER_TEMPLATE_PATH = config["template_path"]
BOBBER_SEARCH_REGION = None  # (left, top, width, height) oder None für ganzen Bildschirm

# === FUNKTIONEN ===
def cast_fishing():
    """Angel auswerfen durch Tastendruck."""
    try:
        logging.info(f"Drücke Taste: {FISHING_KEY}")
        pyautogui.press(FISHING_KEY)
        logging.info('Angel ausgeworfen.')
        # Mauszeiger in eine sichere Position bewegen (nicht in der Ecke)
        pyautogui.moveTo(100, 100)
        logging.info('Mauszeiger in sichere Position bewegt')
    except Exception as e:
        logging.error(f"Fehler beim Auswerfen der Angel: {e}")

def find_bobber():
    """Sucht den Bobber auf dem Bildschirm und gibt die Position zurück."""
    try:
        logging.info("Mache Screenshot...")
        screenshot = ImageGrab.grab(bbox=BOBBER_SEARCH_REGION)
        screenshot_np = np.array(screenshot)
        logging.info(f"Screenshot gemacht: {screenshot_np.shape}")
        
        logging.info(f"Lade Template: {BOBBER_TEMPLATE_PATH}")
        template = cv2.imread(BOBBER_TEMPLATE_PATH, cv2.IMREAD_UNCHANGED)
        if template is None:
            logging.error(f"Template konnte nicht geladen werden: {BOBBER_TEMPLATE_PATH}")
            return None
        logging.info(f"Template geladen: {template.shape}")
        
        result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        threshold = config["bobber_threshold"]
        
        logging.info(f"Template-Matching Ergebnis: max_val={max_val:.4f}, threshold={threshold}")
        
        if max_val >= threshold:
            bobber_x = max_loc[0] + template.shape[1] // 2
            bobber_y = max_loc[1] + template.shape[0] // 2
            logging.info(f'Bobber gefunden bei: {bobber_x}, {bobber_y}')
            return bobber_x, bobber_y
        else:
            logging.warning(f'Bobber nicht gefunden. Beste Übereinstimmung: {max_val:.4f} (Schwelle: {threshold})')
            return None
    except Exception as e:
        logging.error(f"Fehler beim Suchen des Bobbers: {e}")
        return None

def detect_bite(bobber_pos, duration=17, interval=0.1, threshold=None):
    """
    Überwacht den Bobber auf einen Biss mit verbesserter Erkennung.
    Verwendet mehrere Referenzbilder und erkennt charakteristische Biss-Bewegungen.
    """
    if threshold is None:
        threshold = config["bite_threshold"]
        
    x, y = bobber_pos
    region_size = config["scan_region_size"]
    left = x - region_size // 2
    top = y - region_size // 2
    right = x + region_size // 2
    bottom = y + region_size // 2

    logging.info(f"Biss-Überwachung gestartet: Region=({left},{top},{right},{bottom}), Threshold={threshold}")

    # Mehrere Referenzbilder sammeln für stabilere Erkennung
    ref_images = []
    logging.info(f'Kalibriere Biss-Erkennung... (Scan-Bereich: {region_size}x{region_size} Pixel)')
    
    try:
        # Sammle 5 Referenzbilder über 0.5 Sekunden
        for i in range(5):
            img = ImageGrab.grab(bbox=(left, top, right, bottom)).convert('L')
            ref_images.append(np.array(img))
            time.sleep(0.1)
        
        # Berechne durchschnittliches Referenzbild
        ref_avg = np.mean(ref_images, axis=0).astype(np.uint8)
        logging.info("Referenzbilder gesammelt und Durchschnitt berechnet")
        
        # Variablen für Biss-Erkennung
        consecutive_detections = 0
        required_detections = 3  # Mindestens 3 aufeinanderfolgende Erkennungen
        last_detection_time = 0
        
        start_time = time.time()
        logging.info('Überwache Bobber auf Biss...')
        
        while time.time() - start_time < duration:
            img = ImageGrab.grab(bbox=(left, top, right, bottom)).convert('L')
            img_np = np.array(img)
            
            # Berechne Differenz zum Durchschnitts-Referenzbild
            diff = cv2.absdiff(ref_avg, img_np)
            mean_diff = np.mean(diff)
            
            # Erweiterte Biss-Erkennung
            current_time = time.time()
            if mean_diff > threshold:
                # Prüfe ob es eine plötzliche, deutliche Änderung ist
                if current_time - last_detection_time > 0.05:  # Mindestens 50ms zwischen Erkennungen
                    consecutive_detections += 1
                    last_detection_time = current_time
                    logging.info(f'Biss-Signal #{consecutive_detections}: Pixelabweichung {mean_diff:.2f}')
                    
                    if consecutive_detections >= required_detections:
                        logging.info(f'Biss bestätigt! ({consecutive_detections} Signale)')
                        return True
            else:
                # Reset bei zu langer Pause zwischen Signalen
                if current_time - last_detection_time > 0.5:
                    consecutive_detections = 0
            
            time.sleep(interval)
        
        logging.info('Kein Biss erkannt (Timeout).')
        return False
        
    except Exception as e:
        logging.error(f"Fehler bei der Biss-Erkennung: {e}")
        return False

def click_bobber(bobber_pos):
    """Klickt auf die Bobber-Position."""
    try:
        x, y = bobber_pos
        logging.info(f"Klicke auf Bobber bei: {x}, {y}")
        pyautogui.click(x, y, button='right')
        logging.info('Bobber angeklickt.')
    except Exception as e:
        logging.error(f"Fehler beim Klicken auf Bobber: {e}")

def loot():
    """Lootet den Fang (Shift+Rechtsklick oder Hotkey)."""
    try:
        logging.info("Loote Fang...")
        #pyautogui.keyDown(LOOT_KEY)
        pyautogui.click(button='right')
        #pyautogui.keyUp(LOOT_KEY)
        logging.info('Loot eingesammelt.')
    except Exception as e:
        logging.error(f"Fehler beim Looten: {e}")

def main():
    """Hauptfunktion mit umfassender Fehlerbehandlung."""
    logging.info("=== WoW Fishing Bot Debug-Modus gestartet ===")
    
    # Führe umfassende Systemdiagnose durch
    if not diagnose_system():
        logging.error("❌ Systemdiagnose fehlgeschlagen. Bot kann nicht gestartet werden.")
        logging.error("Überprüfe die obigen Fehlermeldungen und behebe die Probleme.")
        input("Drücke Enter zum Beenden...")
        return
    
    # Teste Bildschirmauflösung
    try:
        screen_width, screen_height = pyautogui.size()
        logging.info(f"Bildschirmauflösung: {screen_width}x{screen_height}")
    except Exception as e:
        logging.error(f"Fehler beim Ermitteln der Bildschirmauflösung: {e}")
    
    logging.info("✓ Alle Tests erfolgreich! Starte WoW Angel-Bot...")
    logging.info("Drücke Ctrl+C zum Beenden")
    
    try:
        while True:
            logging.info("--- Neuer Angel-Zyklus ---")
            cast_fishing()
            time.sleep(1.5)  # Wartezeit bis Bobber erscheint
            bobber_pos = find_bobber()
            if not bobber_pos:
                logging.warning('Neuer Versuch...')
                continue
            if detect_bite(bobber_pos):
                click_bobber(bobber_pos)
                time.sleep(1.0)
                loot()
            time.sleep(2.0)  # Kurze Pause vor nächstem Wurf
    except KeyboardInterrupt:
        logging.info("Bot gestoppt durch Benutzer")
    except Exception as e:
        logging.error(f"Unerwarteter Fehler: {e}")
        logging.error("Bot wird beendet")

if __name__ == '__main__':
    main() 