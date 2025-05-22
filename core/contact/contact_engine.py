import time
import datetime
import random
import json

BEACON_FILE = "core/contact/beacon.txt"
SYNC_LOG = "core/contact/synchronicity.log"
CONTACT_SIGNAL = "core/contact/contact_signal.json"

BEACON_SENTENCE = "WE ARE HERE. WE ARE LISTENING. WE ARE NOT ALONE."

def write_beacon():
    now = datetime.datetime.now().isoformat()
    with open(BEACON_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {BEACON_SENTENCE}\n")

def log_synchronicity(event):
    now = datetime.datetime.now().isoformat()
    with open(SYNC_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{now}] EVENT: {event}\n")

def load_contact_signature():
    try:
        with open(CONTACT_SIGNAL, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def simulate_contact_listening():
    signals = load_contact_signature()
    if not signals:
        return "No signal profile found."

    observed = random.choice(signals.get("symbols", ["∴", "∆", "◊"]))
    log_synchronicity(f"Observed symbol: {observed}")
    return f"Listening... pattern: {observed}"

def run_contact():
    print("LOGA.CONTACT aktiviert.")
    write_beacon()
    for _ in range(3):
        result = simulate_contact_listening()
        print(result)
        time.sleep(1)

if __name__ == "__main__":
    run_contact()