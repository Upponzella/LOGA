import os
import datetime
import json
import shutil

POLICY_PATH = "system/mutate/mutate_policy.json"
LOG_PATH = "system/mutate/mutation.log"
HISTORY_PATH = "system/mutate/history/"

def load_policy():
    if not os.path.exists(POLICY_PATH):
        return {"allow_mutation": False}
    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def mutate_file(target_path, new_code):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(target_path)
    backup_path = os.path.join(HISTORY_PATH, f"{filename}.{timestamp}.bak")

    if os.path.exists(target_path):
        shutil.copy2(target_path, backup_path)

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(new_code)

    log_entry = f"[{timestamp}] MUTATED: {target_path} (Backup: {backup_path})\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(log_entry.strip())

def run_mutation():
    policy = load_policy()
    if not policy.get("allow_mutation", False):
        print("[MUTATE] Mutation nicht erlaubt. Vorgang abgebrochen.")
        return

    # Beispielmutation: einfache Änderung an loop_engine.py
    sample_path = "loop/loop_engine.py"
    new_code = "# Automatisch mutiert: neue Version\nprint('Neue LOOP-Version aktiv.')"
    mutate_file(sample_path, new_code)

if __name__ == "__main__":
    run_mutation()
