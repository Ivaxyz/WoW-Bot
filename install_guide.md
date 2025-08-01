# WoW Fishing Bot - Installationsanleitung (.exe Version)

## Voraussetzungen
- Windows 10/11
- Alle Dateien im gleichen Ordner
- **KEINE Python-Installation erforderlich!**

## Installation
1. Alle Dateien in einen Ordner entpacken
2. `WoW Fishing Bot.exe` ausführen
3. Fertig!

## Häufige Probleme und Lösungen

### Problem: "Programm kann nicht gestartet werden"
**Lösung:** 
- Als Administrator ausführen
- Antivirus temporär deaktivieren
- Windows Defender Ausnahme hinzufügen

### Problem: Bot findet Bobber nicht
**Mögliche Ursachen:**
1. Falsche Bildschirmauflösung
2. Unterschiedliche WoW-Grafikeinstellungen
3. Bobber-Template passt nicht

**Lösung:** Neues Bobber-Template erstellen:
1. Screenshot vom Bobber machen
2. Als `bobber_template.png` speichern
3. `config.json` anpassen

### Problem: Bot reagiert nicht auf Bisse
**Lösung:** Schwellenwerte in `config.json` anpassen:
```json
{
    "bobber_threshold": 0.2,
    "bite_threshold": 10,
    "scan_region_size": 60
}
```

### Problem: Tastatureingaben funktionieren nicht
**Lösung:** 
1. WoW im Vordergrund haben
2. Vollbildmodus deaktivieren (Fenster-Modus verwenden)
3. Als Administrator ausführen

## Test-Schritte
1. WoW starten und zum Angeln gehen
2. `WoW Fishing Bot.exe` ausführen
3. Bot sollte "Starte WoW Angel-Bot..." ausgeben
4. Angel auswerfen und testen

## Wichtige Hinweise
- **WoW muss im Vordergrund sein!**
- **Fenster-Modus verwenden (nicht Vollbild)**
- **Als Administrator ausführen falls nötig**
- **Antivirus kann die .exe blockieren** 