# Spoolman Sync

Synchronisiert das Extra-Feld tag und das Feld lot_nr in Spoolman-Filamentspulen.
lot_nr ist führend, d.h. Änderungen werden immer von lot_nr nach tag synchronisiert.
Das Skript ist kompatibel mit Spoolman ab Version 0.22.1 und nutzt eine .env-Datei zur Konfiguration.

## Dank und Inspiration

Dieses Projekt wäre nicht möglich ohne die großartige Vorarbeit folgender Entwickler und Repositories:

- [MrBambuSpoolPal-BambuSpoolPal_AndroidApp](https://github.com/MrBambuSpoolPal/MrBambuSpoolPal-BambuSpoolPal_AndroidApp)
  *Eine Android-App zum Auslesen der Bambu Lab RFID-Tags und automatischen Eintragen in Spoolman.*

- [Donkie/Spoolman](https://github.com/Donkie/Spoolman)
  *Das zentrale Open-Source-Filamentverwaltungssystem, auf dem dieses Projekt aufsetzt.*

- [Rdiger-36/bambulab-ams-spoolman-filamentstatus](https://github.com/Rdiger-36/bambulab-ams-spoolman-filamentstatus)
  *Skripte und Tools zur Integration von Bambu Lab AMS und Spoolman.*

**Vielen Dank an alle Entwickler und die Community für die Inspiration und die hervorragende Vorarbeit!**

---

## Aktueller Funktionsumfang

Mit diesem Projekt werden Filament-Spulen automatisch mit dem Bambu Lab AMS (Automatic Material System) oder per Handy (NFC/RFID) ausgelesen und in Spoolman eingetragen bzw. aktualisiert.

- Die RFID-Chips der Bambu Lab-Spulen werden mit einem NFC-fähigen Android-Gerät und der oben genannten App ausgelesen.
- Die Daten (z.B. Seriennummer, Chargennummer) werden automatisch an Spoolman übertragen.
- Der Filamentverbrauch wird automatisch über das AMS (einschließlich mehrerer AMS-Systeme) in Spoolman aktualisiert.

**Getestet mit:**
- Bambu Lab X1E
- AMS 1
- AMS 2 Pro

---

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

## Nutzung mit virtueller Umgebung (venv)

Es wird empfohlen, das Skript in einer Python-virtuellen Umgebung (venv) auszuführen.  
So stellst du sicher, dass alle Abhängigkeiten sauber installiert sind und keine Konflikte mit Systempaketen entstehen.

**Aktivieren der venv:**
cd /pfad/zu/deinem/projekt
python3 -m venv venv
source venv/bin/activate
pip install python-dotenv requests

**Starten des Skripts (im venv):**
python spoolman-sync.py

# Automatisierung mit Cronjob

**Wichtig:**  
Gib im Cronjob immer den vollständigen Pfad zum Python-Interpreter deiner venv an.  
Du findest ihn mit `which python` im aktivierten venv.

**Beispiel für einen Cronjob (alle 5 Minuten zwischen 6 und 23 Uhr):**
*/5 6-23 * * * /home/username/myproject/venv/bin/python /home/username/myproject/spoolman-sync.py

Ersetze `/home/username/myproject/` durch deinen tatsächlichen Pfad.

**Optional:**  
Um etwaige Fehler und Ausgaben zu protokollieren, kannst du die Ausgabe umleiten:

*/5 6-23 * * * /home/username/myproject/venv/bin/python /home/username/myproject/spoolman-sync.py >> /tmp/spoolman_sync_cron.log 2>&1

### Hinweis

- Die `.env`-Datei muss im selben Verzeichnis wie das Skript liegen, damit die Umgebungsvariablen korrekt geladen werden.
- Wenn du das Skript aus einem anderen Verzeichnis startest oder die `.env` woanders liegt, passe im Skript den Pfad zu `.env` an:
from dotenv import load_dotenv
load_dotenv(dotenv_path='/home/username/myproject/.env')

**Tipp:**  
Wenn du ein Wrapper-Skript verwendest, das die venv aktiviert, stelle sicher, dass es im Cronjob als ausführbar (`chmod +x`) hinterlegt ist.

**Beispiel für einen anonymisierten Pfad:**
*/5 6-23 * * * /home/username/myproject/venv/bin/python /home/username/myproject/spoolman-sync.py

---

**Zusammengefasst:**
- Immer den venv-Python im Cronjob nutzen!
- `.env`-Datei im Skriptverzeichnis belassen
- Optional: Logging der Cron-Ausgabe

## Einrichtung

1. Anpassen/Erstellen der .env Datei und Variablen
2. Ausführen: `python3 spoolman-sync.py`
3. Optional als Cronjob einrichten.

---

## Ausblick

Als nächstes wird eine **Docker-Variante** dieses Projekts entwickelt, um die Integration und den Betrieb noch einfacher und portabler zu machen.

---

**Hinweis:**  
Alle genannten Projekte stehen unter ihren jeweiligen Lizenzen. Bitte beachte die Lizenzbedingungen, wenn du Teile davon weiterverwendest.


## Lizenz

GPL 3 License

