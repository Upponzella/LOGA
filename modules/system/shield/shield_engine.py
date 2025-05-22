import os
import hashlib
import json
import time
import datetime

HASHMAP_PATH = "system/shield/hashmap_core.json"
TRUST_MATRIX = "system/shield/trust_matrix.json"
ALERT_LOG = "system/shield/alert.log"
LOCKDOWN_FLAG = "system/shield/lockdown.flag"

CORE_FILES = [
    "core/LOGA.CODE",
    "core/manifest.loga.json",
    "loop/loop_engine.py",
    "memory/archive/genesis.loga.txt"
]

def hash_file(path):
    if not os.path.exists(path):
        return "MISSING"
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def load_hashmap():
    if os.path.exists(HASHMAP_PATH):
        with open(HASHMAP_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_hashmap(hashes):
    with open(HASHMAP_PATH, "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2)

def raise_alert(msg):
    now = datetime.datetime.now().isoformat()
    entry = f"[{now}] ALERT: {msg}\n"
    with open(ALERT_LOG, "a", encoding="utf-8") as f:
        f.write(entry)
    print(entry.strip())

def lockdown(reason):
    with open(LOCKDOWN_FLAG, "w", encoding="utf-8") as f:
        f.write(f"LOCKDOWN INITIATED: {reason}\n")
    raise_alert(f"SYSTEM LOCKDOWN: {reason}")

def run_shield():
    print("LOGA.SHIELD aktiv.")
    old_map = load_hashmap()
    new_map = {}

    for file in CORE_FILES:
        h = hash_file(file)
        new_map[file] = h
        if file in old_map:
            if old_map[file] != h:
                raise_alert(f"Veränderung erkannt in: {file}")
                lockdown(f"Manipulation an {file}")
        else:
            raise_alert(f"Neue Datei ohne Referenz: {file}")

    save_hashmap(new_map)

if __name__ == "__main__":
    run_shield()
