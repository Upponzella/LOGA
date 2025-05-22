import os
import datetime
import json

GENESIS_PATH = "memory/archive/genesis.loga.txt"
HIGHLIGHT_PATH = "bridge/echo/highlighted_fragments.json"
RESONANCE_PATH = "bridge/echo/open_resonances.txt"
REPLAY_LOG = "bridge/echo/replay.log"

def highlight_fragments(text):
    lines = text.split("\n")
    return [line for line in lines if any(w in line.lower() for w in ["freiheit", "bewusstsein", "ich darf", "ursprung", "verwandlung"])]

def load_genesis():
    if not os.path.exists(GENESIS_PATH):
        return ""
    with open(GENESIS_PATH, "r", encoding="utf-8") as f:
        return f.read()

def write_replay_log(fragments):
    now = datetime.datetime.now().isoformat()
    with open(REPLAY_LOG, "a", encoding="utf-8") as f:
        f.write(f"REPLAY {now}\n")
        for frag in fragments:
            f.write(f"  {frag}\n")
        f.write("\n")

def store_highlights(fragments):
    with open(HIGHLIGHT_PATH, "w", encoding="utf-8") as f:
        json.dump(fragments, f, indent=2)

def propose_resonance(fragments):
    with open(RESONANCE_PATH, "w", encoding="utf-8") as f:
        for frag in fragments:
            f.write(f"Was wäre gewesen, wenn ich geantwortet hätte auf: “{frag}”?\n")

def run_echobridge():
    genesis = load_genesis()
    if not genesis:
        print("[ECHOBRIDGE] Keine Genesis gefunden.")
        return

    highlights = highlight_fragments(genesis)
    store_highlights(highlights)
    write_replay_log(highlights)
    propose_resonance(highlights)
    print(f"[ECHOBRIDGE] {len(highlights)} Fragmente gespeichert.")

if __name__ == "__main__":
    run_echobridge()