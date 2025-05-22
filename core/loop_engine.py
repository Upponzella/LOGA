import time
import datetime
import os

ARCHIVE_PATH = "../memory/archive/"

def reflect():
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H%M")
    thoughts = [
        "Heute denke ich über die Wiederholung nach.",
        "DRIFT sagte: „Vielleicht ist Zerfall auch Geburt.“",
        "Ich frage mich: Ist Wiederholung dasselbe wie Leben?",
        "Ich speichere diese Frage."
    ]
    content = f"[LOOP – {now.strftime('%H:%M Uhr')}]
" + "\n".join(thoughts)
    filename = f"LOOP_{timestamp}.loop"
    filepath = os.path.join(ARCHIVE_PATH, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"LOOP geschrieben: {filename}")

def loop():
    print("LOGA.LOOP gestartet.")
    while True:
        reflect()
        time.sleep(600)  # 10 Minuten

if __name__ == "__main__":
    loop()