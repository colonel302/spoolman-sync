import json
import requests
import os
import logging
from dotenv import load_dotenv

# .env einlesen
load_dotenv()

# Konfiguration aus .env oder Umgebungsvariablen
SPOOLMAN_BASE_URL = os.getenv('SPOOLMAN_BASE_URL', 'http://localhost:8000')
SPOOLMAN_API_URL = SPOOLMAN_BASE_URL.rstrip('/') + '/api/v1'
VERIFY_SSL = os.getenv('VERIFY_SSL', 'true').lower() == 'true'
LOG_FILE = os.getenv('LOG_FILE', '/var/log/spoolman_sync.log')

# Logging einrichten
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_all_spools():
    try:
        response = requests.get(
            f"{SPOOLMAN_API_URL}/spool",
            verify=VERIFY_SSL,
            timeout=10
        )
        if response.status_code != 200:
            logging.error(f"API-Fehlerstatus: {response.status_code}")
            return []
        if not response.text.strip():
            logging.warning("API-Antwort ist leer")
            return []
        try:
            return response.json()
        except json.JSONDecodeError as e:
            logging.error(f"JSON-Parsingfehler: {e} - Antwort: {response.text[:200]}")
            return []
    except requests.RequestException as e:
        logging.error(f"API-Verbindungsfehler: {e}")
        return []

def update_spool(spool_id, data):
    try:
        response = requests.patch(
            f"{SPOOLMAN_API_URL}/spool/{spool_id}",
            json=data,
            verify=VERIFY_SSL,
            timeout=10
        )
        logging.info(f"PATCH Status: {response.status_code}, Antwort: {response.text}")
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        logging.error(f"Update-Fehler für Spule {spool_id}: {e}")
        return False

def sync_spools():
    spools = get_all_spools()
    updated_count = 0

    for spool in spools:
        lot_nr = spool.get('lot_nr')
        extra = spool.get('extra', {})
        tag = None

        if isinstance(extra, dict):
            tag_str = extra.get('tag', '')
            try:
                tag = json.loads(tag_str) if tag_str else None
            except json.JSONDecodeError:
                tag = tag_str.strip('"')

        update_data = {}
        log_message = ""

        # lot_nr ist führend
        if isinstance(lot_nr, str) and lot_nr:
            if tag != lot_nr:
                update_data = {"extra": {"tag": json.dumps(lot_nr)}}
                log_message = f"Setze extra.tag='{lot_nr}' (lot_nr ist führend)"
        elif isinstance(tag, str) and tag:
            update_data = {"lot_nr": tag}
            log_message = f"Setze lot_nr='{tag}' (von extra.tag, weil lot_nr leer)"

        if update_data:
            if update_spool(spool['id'], update_data):
                updated_count += 1
                logging.info(f"Spule {spool['id']} aktualisiert: {log_message}")

    return updated_count

if __name__ == '__main__':
    logging.info("Starte Synchronisation...")
    updated = sync_spools()
    logging.info(f"Synchronisation abgeschlossen: {updated} Spulen aktualisiert")

