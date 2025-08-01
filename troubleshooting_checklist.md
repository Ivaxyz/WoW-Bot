# WoW Fishing Bot - Troubleshooting Checkliste

## Problem: Bot macht gar nichts (nicht mal Taste 1 drücken)

### 1. **Python und Abhängigkeiten prüfen**
```bash
# Führe die Debug-Version aus
python wow_fishing_bot_debug.py
```

Die Debug-Version wird automatisch:
- ✅ Alle benötigten Python-Pakete installieren
- ✅ Fehlende Dateien erstellen
- ✅ WoW-Fenster finden und aktivieren
- ✅ Tastatureingaben testen

### 2. **Manuelle Schritte (falls Debug-Version nicht funktioniert)**

#### A) Python-Pakete installieren
```bash
pip install pyautogui opencv-python numpy pillow
```

#### B) Als Administrator ausführen
- Rechtsklick auf `wow_fishing_bot_debug.py`
- "Als Administrator ausführen" wählen

#### C) WoW-Fenster aktivieren
- Stelle sicher, dass WoW läuft
- Klicke in das WoW-Fenster, damit es aktiv ist
- Der Bot kann nur in das aktive Fenster Tastatureingaben senden

#### D) Antivirus-Software prüfen
- Deaktiviere temporär Antivirus-Software
- Oder füge den Bot-Ordner zu den Ausnahmen hinzu

### 3. **Häufige Fehlermeldungen und Lösungen**

#### "Kein WoW-Fenster gefunden"
- ✅ WoW starten
- ✅ Sicherstellen, dass WoW läuft
- ✅ Fenster-Titel prüfen (sollte "World of Warcraft" enthalten)

#### "Berechtigungsproblem"
- ✅ Als Administrator ausführen
- ✅ Antivirus-Software deaktivieren
- ✅ Windows Defender Ausnahmen hinzufügen

#### "Tastatureingabe fehlgeschlagen"
- ✅ WoW-Fenster aktivieren (hineinklicken)
- ✅ Vollbildmodus deaktivieren (Fenster-Modus verwenden)
- ✅ Andere Programme schließen, die Tastatureingaben abfangen

#### "Template konnte nicht geladen werden"
- ✅ `bobber_template.png` Datei prüfen
- ✅ Debug-Version erstellt automatisch ein Test-Template

### 4. **Erweiterte Fehlerbehebung**

#### A) Vollbildmodus Problem
- WoW in Fenster-Modus starten
- Oder Alt+Tab verwenden, um zwischen Fenstern zu wechseln

#### B) Tastatur-Layout
- Stelle sicher, dass die Taste "1" auf der Tastatur funktioniert
- Teste manuell in WoW, ob die Angel-Taste funktioniert

#### C) Bildschirmauflösung
- Verwende Standard-Auflösungen (1920x1080, 1366x768)
- Skalierung auf 100% setzen

### 5. **Test-Schritte**

1. **Starte Debug-Version:**
   ```bash
   python wow_fishing_bot_debug.py
   ```

2. **Folge den Anweisungen:**
   - Der Bot wird automatisch alle Tests durchführen
   - Bei Problemen werden spezifische Lösungen angezeigt

3. **Manueller Test:**
   - Starte WoW
   - Aktiviere das WoW-Fenster
   - Drücke manuell "1" - sollte Angel auswerfen
   - Wenn das funktioniert, sollte der Bot auch funktionieren

### 6. **Log-Datei prüfen**
- Öffne `bot_debug.log` nach dem Ausführen
- Suche nach Fehlermeldungen
- Die Log-Datei zeigt genau, wo das Problem liegt

### 7. **Alternative: GUI-Version**
Falls die Kommandozeilen-Version nicht funktioniert:
```bash
python wow_fishing_bot_gui.py
```

## Häufige Lösungen nach Fehlertyp:

### ❌ "ImportError: No module named 'pyautogui'"
**Lösung:** `pip install pyautogui`

### ❌ "Permission denied"
**Lösung:** Als Administrator ausführen

### ❌ "WoW-Fenster nicht gefunden"
**Lösung:** WoW starten und Fenster aktivieren

### ❌ "Tastatureingabe funktioniert nicht"
**Lösung:** WoW-Fenster in den Vordergrund bringen

### ❌ "Template-Datei fehlt"
**Lösung:** Debug-Version erstellt automatisch ein Test-Template

---

**Wichtig:** Die Debug-Version (`wow_fishing_bot_debug.py`) ist die beste Wahl für die Fehlerbehebung, da sie automatisch alle Probleme erkennt und behebt! 