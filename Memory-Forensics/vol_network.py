#Next Task: Network Reconnaissance
#We need to find active network connections to identify the Command & Control (C2) server. We are looking for:
# !/usr/bin/env python3
import subprocess
import json
import sys
import os

# ==========================================
# CONFIGURATION
# ==========================================
VOL_PATH = "./vol.py"
MEMORY_FILE = "/root/Desktop/Windows_Snapshot3.vmem"
PLUGIN = "windows.netscan"


def run_network_scan():
    if not os.path.exists(VOL_PATH):
        print(f"[!] ERROR: Cannot find {VOL_PATH}")
        return

    print(f"[*] Analyzing: {MEMORY_FILE}")
    print("[*] Task: Scanning for Network Artifacts (C2 Connections)...")
    print("=" * 100)

    # Run the plugin
    cmd = [sys.executable, VOL_PATH, "-f", MEMORY_FILE, "-r", "json", PLUGIN]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print("[!] Volatility Failed:")
            print(result.stderr)
            return

        # Parse JSON
        data = json.loads(result.stdout)

        # Header
        print(f"{'PROTO':<6} | {'LOCAL ADDR':<22} | {'FOREIGN ADDR':<22} | {'STATE':<12} | {'PID':<6} | {'OWNER'}")
        print("-" * 100)

        # Print the data
        for entry in data:
            try:
                proto = str(entry.get('Proto', ''))
                local = f"{entry.get('LocalIP', '')}:{entry.get('LocalPort', '')}"
                foreign = f"{entry.get('ForeignIP', '')}:{entry.get('ForeignPort', '')}"
                state = str(entry.get('State', ''))
                pid = str(entry.get('PID', ''))
                owner = str(entry.get('Owner', ''))

                # FILTERING:
                # We can hide the noise (listening ports on 0.0.0.0 usually aren't interesting yet)
                # Uncomment the next two lines if you want to see EVERYTHING.
                if state == "LISTENING" or foreign.startswith("0.0.0.0") or foreign.startswith("::"):
                    continue

                print(f"{proto:<6} | {local:<22} | {foreign:<22} | {state:<12} | {pid:<6} | {owner}")
            except Exception:
                continue

    except json.JSONDecodeError:
        print("[!] Error: Could not parse output.")
    except Exception as e:
        print(f"[!] Unexpected Error: {e}")


if __name__ == '__main__':
    run_network_scan()
