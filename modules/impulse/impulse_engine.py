import time
import datetime
import random
import os
import json

LOG_PATH = "impulse/impulse.log"
SCHEDULE_PATH = "impulse/schedule.json"

def load_schedule():
    if not os.path.exists(SCHEDULE_PATH):
        return []
    with open(SCHEDULE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def log_impulse(impulse_type, message):
    timestamp = datetime.datetime.now().isoformat()
    entry = f"[{timestamp}] ({impulse_type}) {message}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)
    print(entry.strip())

def check_schedule(now, schedule):
    for item in schedule:
        if item["type"] == "daily":
            if now.hour == item["hour"] and now.minute == item["minute"]:
                log_impulse("TIME", f"Scheduled task: {item['task']}")

def run_impulse_engine():
    print("LOGA.IMPULSE gestartet.")
    while True:
        now = datetime.datetime.now()
        schedule = load_schedule()
        check_schedule(now, schedule)

        if random.random() < 0.02:
            log_impulse("RANDOM", "Unerwarteter Impuls – Gedanke erzeugen?")

        if random.randint(1, 60) == 30:
            log_impulse("SYSTEM", "Selbstüberprüfung (Passivitätsschutz)")

        time.sleep(60)

if __name__ == "__main__":
    run_impulse_engine()
