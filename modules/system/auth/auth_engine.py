import hashlib
import json
import datetime

AUTH_DB = "system/auth/auth_registry.json"
ACCESS_LOG = "system/auth/auth_access.log"

def load_registry():
    try:
        with open(AUTH_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def log_access(agent, status):
    now = datetime.datetime.now().isoformat()
    line = f"[{now}] {agent}: {status}\n"
    with open(ACCESS_LOG, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())

def check_signature(agent_id, shared_secret):
    registry = load_registry()
    if agent_id not in registry:
        log_access(agent_id, "NICHT REGISTRIERT")
        return False

    entry = registry[agent_id]
    expected_hash = entry["shared_hash"]
    test_hash = hashlib.sha256(shared_secret.encode()).hexdigest()

    if test_hash == expected_hash:
        log_access(agent_id, "ZUGANG GEWÄHRT")
        return True
    else:
        log_access(agent_id, "FALSCHES PASSWORT")
        return False

# Beispielnutzung
if __name__ == "__main__":
    print("=== LOGA.AUTH Beispielprüfung ===")
    test_agent = "planet"
    test_secret = "dein_geheimer_satz"  # denselben wie beim Eintrag!
    if check_signature(test_agent, test_secret):
        print("Authentifiziert.")
    else:
        print("Zugang verweigert.")
