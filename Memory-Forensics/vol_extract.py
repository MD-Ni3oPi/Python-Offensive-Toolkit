#!/usr/bin/env python3
import subprocess
import json
import sys
import os

# ==========================================
# CONFIGURATION
# ==========================================
VOL_PATH = "./vol.py"
MEMORY_FILE = "/root/Desktop/Windows_Snapshot3.vmem"

# The list of plugins to tryc
PLUGINS = [
    "windows.cachedump",
    "windows.lsadump",
    "windows.envars"
]


def run_hunter():
    if not os.path.exists(VOL_PATH):
        print(f"[!] ERROR: Cannot find {VOL_PATH}")
        return

    print(f"[*] attacking memory file: {MEMORY_FILE}")
    print("=" * 60)

    for plugin in PLUGINS:
        print(f"[*] Running plugin: {plugin}...")

        # Construct command
        cmd = [sys.executable, VOL_PATH, "-f", MEMORY_FILE, "-r", "json", plugin]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"[-] {plugin} failed to run.")
                continue

            # Parse JSON
            try:
                data = json.loads(result.stdout)
            except json.JSONDecodeError:
                # Sometimes plugins return empty text instead of JSON []
                print(f"[-] {plugin} returned no data.")
                continue

            if not data:
                print(f"[-] {plugin} ran but found nothing.")
                continue

            # SUCCESS!
            print(f"[+] {plugin} FOUND DATA!")
            print("-" * 60)

            # Smart Print based on Plugin
            if plugin == "windows.cachedump":
                for entry in data:
                    user = entry.get('Username', 'N/A')
                    h = entry.get('Hash', 'N/A')
                    print(f"    User: {user:<15} | Hash: {h}")

            elif plugin == "windows.lsadump":
                for entry in data:
                    key = entry.get('Key', 'N/A')
                    secret = entry.get('Secret', 'N/A')
                    print(f"    Key: {key:<20} | Secret: {secret}")

            elif plugin == "windows.envars":
                # Filter for interesting variables
                interesting = ['PASS', 'KEY', 'SECRET', 'TOKEN', 'USER', 'ADMIN']
                for entry in data:
                    var = str(entry.get('Variable', '')).upper()
                    val = str(entry.get('Value', ''))
                    # Only print if it looks sensitive
                    if any(x in var for x in interesting):
                        pid = entry.get('PID', 'N/A')
                        print(f"    PID: {pid:<6} | {var} = {val}")

            print("=" * 60)
            print("\n")

        except Exception as e:
            print(f"[!] Error running {plugin}: {e}")


if __name__ == '__main__':
    run_hunter()
