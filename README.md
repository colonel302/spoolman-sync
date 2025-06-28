# Spoolman Sync

Synchronisiert das Extra-Feld tag und das Feld lot_nr in Spoolman-Filamentspulen.
lot_nr ist führend, d.h. Änderungen werden immer von lot_nr nach tag synchronisiert.
Das Skript ist kompatibel mit Spoolman ab Version 0.22.1 und nutzt eine .env-Datei zur Konfiguration.

## Voraussetzungen

- Python 3
- requests (`pip install requests`)
- python-dotenv (pip install python-dotenv)
- Zugriff auf eine Spoolman-Instanz (getestet mit v0.22.1)

## Konfiguration

Lege im Projektverzeichnis eine .env-Datei an (siehe Beispiel).
Wichtig: Die Datei .env darf sensible Informationen enthalten und sollte nicht öffentlich geteilt werden.

Beispiel: .env.example

### Basis-URL deiner Spoolman-Instanz (ohne /api/v1 am Ende)
SPOOLMAN_BASE_URL=http://192.168.x.x:7912

### SSL-Überprüfung aktivieren (true/false)
VERIFY_SSL=true

### Pfad zur Logdatei
LOG_FILE=/var/log/spoolman_sync.log


## Einrichtung

1. Anpassen/Erstellen der .env Datei und Variablen
2. Ausführen: `python3 spoolman-sync.py`
3. Optional als Cronjob einrichten.

### Cronjob Beispiel

Um das Skript regelmäßig auszuführen, z.B. alle 5 Minuten zwischen 6 und 23 Uhr:

*/5 6-23 * * * /usr/bin/python3 /pfad/zu/spoolman-sync/spoolman-sync.py

## Lizenz

GPL 3 License

