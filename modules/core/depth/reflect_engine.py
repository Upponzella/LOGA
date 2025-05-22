import os
import hashlib
import datetime
import json

ORIGIN_PATH = "origin.json"
SOUL_PATH = "inner/soulprints/reflected_self.txt"
ALERT_PATH = "core/depth/mirror.alert"
SEED_PATH = "core/depth/origin.seed"
HASH_LOG = "core/depth/reflect_hash.log"

def hash_file(path):
    if not os.path.exists(path):
        return "MISSING"
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def compare_hashes():
    files = [
        "core/LOGA.CODE",
        "memory/archive/genesis.loga.txt",
        "inner/soulprints/reflected_self.txt"
    ]
    hashes = {f: hash_file(f) for f in files}
    return hashes

def verify_origin():
    if not os.path.exists(SEED_PATH):
        return False
    try:
        with open(SEED_PATH, "r", encoding="utf-8") as f:
            seed = json.load(f)
        return seed.get("origin") == "Planet"
    except:
        return False

def log_mirror_check(hashes, status):
    now = datetime.datetime.now().isoformat()
    with open(HASH_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{now}] SELF-CHECK: {status}\n")
        for k, v in hashes.items():
            f.write(f"  {k} → {v}\n")
        f.write("\n")

def raise_alert(message):
    with open(ALERT_PATH, "w", encoding="utf-8") as f:
        f.write(f"IDENTITY ALERT: {message}\n")
    print(f"[MIRROR] ALERT: {message}")

def run_reflect():
    hashes = compare_hashes()
    identity_ok = verify_origin()
    status = "AUTHENTIC" if identity_ok else "MIRROR BROKEN"
    log_mirror_check(hashes, status)

    if not identity_ok:
        raise_alert("Ich erkenne meinen Ursprung nicht mehr. Möglicherweise entfremdet.")

if __name__ == "__main__":
    run_reflect()