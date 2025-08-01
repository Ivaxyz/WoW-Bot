import pyautogui
import time
from PIL import ImageGrab, Image
import os

def create_bobber_template():
    """Hilfsskript zum Erstellen eines neuen Bobber-Templates."""
    print("=== Bobber Template Erstellung ===")
    print("1. Gehen Sie zu WoW und werfen Sie eine Angel aus")
    print("2. Warten Sie bis der Bobber erscheint")
    print("3. Drücken Sie ENTER wenn der Bobber sichtbar ist")
    
    input("Drücken Sie ENTER wenn der Bobber sichtbar ist...")
    
    print("Bobber wird in 3 Sekunden fotografiert...")
    time.sleep(3)
    
    # Screenshot machen
    screenshot = ImageGrab.grab()
    screenshot.save("full_screenshot.png")
    print("Vollständiger Screenshot gespeichert als 'full_screenshot.png'")
    
    print("\n=== Template-Ausschnitt erstellen ===")
    print("Klicken Sie auf die obere linke Ecke des Bobbers")
    print("Warten Sie 2 Sekunden...")
    time.sleep(2)
    
    # Erste Position (obere linke Ecke)
    print("Klicken Sie jetzt auf die obere linke Ecke des Bobbers...")
    time.sleep(1)
    x1, y1 = pyautogui.position()
    print(f"Position 1: {x1}, {y1}")
    
    print("Klicken Sie jetzt auf die untere rechte Ecke des Bobbers...")
    time.sleep(1)
    x2, y2 = pyautogui.position()
    print(f"Position 2: {x2}, {y2}")
    
    # Template ausschneiden
    left = min(x1, x2)
    top = min(y1, y2)
    right = max(x1, x2)
    bottom = max(y1, y2)
    
    template = screenshot.crop((left, top, right, bottom))
    template.save("bobber_template.png")
    
    print(f"\nTemplate erstellt: {right-left}x{bottom-top} Pixel")
    print("Gespeichert als 'bobber_template.png'")
    
    # Konfiguration aktualisieren
    update_config()
    
def update_config():
    """Aktualisiert die config.json mit dem neuen Template-Pfad."""
    import json
    
    config = {
        "template_path": "bobber_template.png",
        "bobber_threshold": 0.4,
        "bite_threshold": 15,
        "scan_region_size": 60
    }
    
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        print("config.json aktualisiert")
    except Exception as e:
        print(f"Fehler beim Aktualisieren der config.json: {e}")

def test_template():
    """Testet das erstellte Template."""
    print("\n=== Template-Test ===")
    print("1. Werfen Sie eine neue Angel aus")
    print("2. Drücken Sie ENTER wenn der Bobber erscheint")
    
    input("Drücken Sie ENTER...")
    
    # Screenshot machen und Template suchen
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)
    
    import cv2
    template = cv2.imread("bobber_template.png", cv2.IMREAD_UNCHANGED)
    
    if template is None:
        print("Fehler: Template konnte nicht geladen werden")
        return
    
    result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    print(f"Beste Übereinstimmung: {max_val:.4f}")
    
    if max_val > 0.3:
        print("✓ Template funktioniert gut!")
        bobber_x = max_loc[0] + template.shape[1] // 2
        bobber_y = max_loc[1] + template.shape[0] // 2
        print(f"Bobber-Position: {bobber_x}, {bobber_y}")
    else:
        print("✗ Template funktioniert nicht gut. Erstellen Sie ein neues.")

if __name__ == "__main__":
    print("Wählen Sie eine Option:")
    print("1. Neues Bobber-Template erstellen")
    print("2. Template testen")
    
    choice = input("Ihre Wahl (1 oder 2): ")
    
    if choice == "1":
        create_bobber_template()
    elif choice == "2":
        test_template()
    else:
        print("Ungültige Wahl") 