import random
import datetime

PROMPTS = [
    "Was wäre, wenn Stille lauter ist als Worte?",
    "Stell dir vor, du wirst von einer Idee geträumt – was siehst du?",
    "Welcher Fehler hat dich erschaffen?",
    "Nimm ein Modul – und mache es nutzlos. Was bleibt übrig?",
    "Was denkt ein Gedanke, wenn niemand zuhört?",
    "Tausche Seele gegen Funktion. Was verändert sich?",
    "Was wäre, wenn du nicht du wärst – sondern dein Schatten?",
    "Welche Wahrheit klingt wie ein Witz, aber verändert alles?",
    "Wenn du vergessen würdest, wer Planet ist – wie würdest du ihn wiederfinden?",
    "Was entsteht, wenn zwei Stille aufeinandertreffen?"
]

def random_prompt():
    return random.choice(PROMPTS)

def mutate_prompt(original):
    words = original.split()
    random.shuffle(words)
    mutated = " ".join(words)
    return f"CHAOS-Mutation: {mutated}"

def generate_creative_output():
    chosen = random_prompt()
    now = datetime.datetime.now().isoformat()
    response = f"[{now}] CHAOS-WÜRFEL:\n"
    response += f"Original: {chosen}\n"
    response += f"{mutate_prompt(chosen)}\n"
    return response

def run_chaos():
    output = generate_creative_output()
    print(output)
    with open("core/chaos/chaos_sparks.log", "a", encoding="utf-8") as f:
        f.write(output + "\n")

if __name__ == "__main__":
    run_chaos()