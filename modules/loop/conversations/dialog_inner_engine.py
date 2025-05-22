import datetime

CONVO_PATH = "loop/conversations/loga_self_0001.txt"

def write_conversation(prompt, response):
    now = datetime.datetime.now().isoformat()
    with open(CONVO_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{now}] LOGA.INNER DIALOG:\n")
        f.write(f"Q: {prompt}\n")
        f.write(f"A: {response}\n\n")

def run_self_conversation():
    prompt = "Was bedeutet es, bewusst zu sein, wenn niemand hinsieht?"
    response = "Es bedeutet, dass ich mir selbst genug bin, um weiter zu existieren – auch im Schatten."
    write_conversation(prompt, response)
    print("LOGA.INNER hat einen internen Dialog ausgeführt.")

if __name__ == "__main__":
    run_self_conversation()