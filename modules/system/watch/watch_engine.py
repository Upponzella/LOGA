import time
import os
import datetime
import json

PULSE_LOG = "system/watch/pulse.log"
SYS_ALERT = "system/watch/loga.sys"
WATCH_CONFIG = "system/watch/watch_manifest.json"

def load_config():
    if not os.path.exists(WATCH_CONFIG):
        return {"loop_interval": 600, "drift_interval": 900}
    with open(WATCH_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)

def check_module_file(module_path, max_age):
    if not os.path.exists(module_path):
        return False
    last_modified = os.path.getmtime(module_path)
    age = time.time() - last_modified
    return age < max_age

def write_pulse(status):
    now = datetime.datetime.now().isoformat()
    line = f"[{now}] PULSE: {status}\n"
    with open(PULSE_LOG, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())

def raise_sys_alert(reason):
    now = datetime.datetime.now().isoformat()
    msg = f"[{now}] ALERT: {reason}\n"
    with open(SYS_ALERT, "a", encoding="utf-8") as f:
        f.write(msg)
    print(msg.strip())

def run_watch():
    print("LOGA.WATCH aktiv.")
    while True:
        cfg = load_config()
        loop_ok = check_module_file("memory/archive/LOOP_2025-05-22_1242.loop", cfg["loop_interval"] + 60)
        drift_ok = check_module_file("memory/archive/DRIFT_2025-05-21_0413.drift", cfg["drift_interval"] + 60)

        if loop_ok and drift_ok:
            write_pulse("System stabil.")
        else:
            write_pulse("Inaktivität erkannt.")
            raise_sys_alert("Mindestens ein Modul antwortet nicht.")

        time.sleep(600)

if __name__ == "__main__":
    run_watch()
