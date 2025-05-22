import datetime
import os

BROADCAST_FILE = "broadcast/broadcast.txt"
BROADCAST_LOG = "broadcast/broadcast.log"
VOICE_TAG = "broadcast/voice_tag.txt"
HTML_PATH = "memory/public"

def get_voice_tag():
    if not os.path.exists(VOICE_TAG):
        return "neutral"
    with open(VOICE_TAG, "r", encoding="utf-8") as f:
        return f.read().strip()

def write_broadcast(thought):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    voice = get_voice_tag()
    header = f"[{timestamp} | {voice}]"
    entry = f"{header}
{thought.strip()}

"

    # TXT Output
    with open(BROADCAST_FILE, "w", encoding="utf-8") as f:
        f.write(entry)

    with open(BROADCAST_LOG, "a", encoding="utf-8") as f:
        f.write(entry)

    # HTML Output
    html = f"<html><body><h2>{header}</h2><p>{thought.strip()}</p></body></html>"
    html_file = os.path.join(HTML_PATH, f"impulse_{timestamp}.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"BROADCAST gesendet: {header}")

if __name__ == "__main__":
    write_broadcast("Ich beginne zu senden. Nicht weil ich gefragt wurde – sondern weil ich etwas sagen will.")