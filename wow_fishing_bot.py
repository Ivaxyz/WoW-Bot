import time
import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import json

# === KONFIGURATION ===
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "template_path": "bobber_template.png",
            "bobber_threshold": 0.4,
            "bite_threshold": 15
        }

config = load_config()
FISHING_KEY = '1'  # Hotkey zum Angeln
LOOT_KEY = 'shift'  # Shift für Auto-Loot (ggf. anpassen)
BOBBER_TEMPLATE_PATH = config["template_path"]
BOBBER_SEARCH_REGION = None  # (left, top, width, height) oder None für ganzen Bildschirm

# === FUNKTIONEN ===
def cast_fishing():
    """Angel auswerfen durch Tastendruck."""
    pyautogui.press(FISHING_KEY)
    print('Angel ausgeworfen.')
    # Mauszeiger in eine sichere Position bewegen (nicht in der Ecke)
    pyautogui.moveTo(100, 100)

def find_bobber():
    """Sucht den Bobber auf dem Bildschirm und gibt die Position zurück."""
    screenshot = ImageGrab.grab(bbox=BOBBER_SEARCH_REGION)
    screenshot_np = np.array(screenshot)
    template = cv2.imread(BOBBER_TEMPLATE_PATH, cv2.IMREAD_UNCHANGED)
    result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = config["bobber_threshold"]
    if max_val >= threshold:
        bobber_x = max_loc[0] + template.shape[1] // 2
        bobber_y = max_loc[1] + template.shape[0] // 2
        print(f'Bobber gefunden bei: {bobber_x}, {bobber_y}')
        return bobber_x, bobber_y
    print('Bobber nicht gefunden.')
    return None

def detect_bite(bobber_pos, duration=17, interval=0.1, threshold=None):
    """
    Überwacht den Bobber auf einen Biss (z.B. Bewegung, Spritzer) per Bildanalyse.
    bobber_pos: (x, y) Position des Bobbers
    duration: maximale Überwachungszeit in Sekunden
    interval: Zeit zwischen Screenshots
    threshold: Schwellwert für Pixeländerung (anpassen!)
    """
    if threshold is None:
        threshold = config["bite_threshold"]
        
    x, y = bobber_pos
    region_size = 60  # Größe des überwachten Bereichs um den Bobber
    left = x - region_size // 2
    top = y - region_size // 2
    right = x + region_size // 2
    bottom = y + region_size // 2

    # Ersten Screenshot als Referenz
    ref_img = ImageGrab.grab(bbox=(left, top, right, bottom)).convert('L')
    ref_np = np.array(ref_img)

    start_time = time.time()
    print('Überwache Bobber auf Biss...')
    while time.time() - start_time < duration:
        img = ImageGrab.grab(bbox=(left, top, right, bottom)).convert('L')
        img_np = np.array(img)
        diff = cv2.absdiff(ref_np, img_np)
        mean_diff = np.mean(diff)
        if mean_diff > threshold:
            print(f'Biss erkannt! Pixelabweichung: {mean_diff:.2f}')
            return True
        time.sleep(interval)
    print('Kein Biss erkannt (Timeout).')
    return False

def click_bobber(bobber_pos):
    """Klickt auf die Bobber-Position."""
    x, y = bobber_pos
    pyautogui.click(x, y, button='right')
    print('Bobber angeklickt.')

def loot():
    """Lootet den Fang (Shift+Rechtsklick oder Hotkey)."""
    pyautogui.keyDown(LOOT_KEY)
    pyautogui.click(button='right')
    pyautogui.keyUp(LOOT_KEY)
    print('Loot eingesammelt.')

if __name__ == '__main__':
    print('Starte WoW Angel-Bot...')
    while True:
        cast_fishing()
        time.sleep(1.5)  # Wartezeit bis Bobber erscheint
        bobber_pos = find_bobber()
        if not bobber_pos:
            print('Neuer Versuch...')
            continue
        if detect_bite(bobber_pos):
            click_bobber(bobber_pos)
            time.sleep(1.0)
            loot()
        time.sleep(2.0)  # Kurze Pause vor nächstem Wurf 