# !/usr/bin/env python3
#We will use the windows.hashdump plugin. (Remember, we fixed the pycryptodome dependency earlier, so this should work now).

import subprocess
import json
import sys
import os

# ==========================================
# CONFIGURATION
# ==========================================
VOL_PATH = "./vol.py"
MEMORY_FILE = "/root/Desktop/Windows_Snapshot3.vmem"

# CHANGE: We switched from 'pslist' to 'hashdump'
PLUGIN = "windows.hashdump"


def run_hashdump():
    if not os.path.exists(VOL_PATH):
        print(f"[!] ERROR: Cannot find {VOL_PATH}")
        return

    print(f"[*] attacking memory file: {MEMORY_FILE}")
    print("[*] Running windows.hashdump... (This extracts NTLM hashes)")

    # 1. Run the Command
    cmd = [sys.executable, VOL_PATH, "-f", MEMORY_FILE, "-r", "json", PLUGIN]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print("[!] Volatility Failed:")
            print(result.stderr)
            return

        # 2. Parse the JSON
        data = json.loads(result.stdout)

        print("\n[+] CREDENTIALS FOUND:")
        print("=" * 80)
        print(f"{'USER':<20} | {'RID':<10} | {'LM HASH':<34} | {'NTLM HASH'}")
        print("=" * 80)

        # 3. Print the Loot
        for entry in data:
            try:
                user = entry.get('User', 'N/A')
                rid = entry.get('RID', 'N/A')
                lm = entry.get('LMHash', 'N/A')
                ntlm = entry.get('NTLMHash', 'N/A')

                print(f"{str(user):<20} | {str(rid):<10} | {str(lm):<34} | {str(ntlm)}")
            except AttributeError:
                continue

    except json.JSONDecodeError:
        print("[!] Error: Output was not valid JSON. (Did the plugin fail?)")
        print("Raw Output:", result.stdout)


if __name__ == '__main__':
    run_hashdump()
