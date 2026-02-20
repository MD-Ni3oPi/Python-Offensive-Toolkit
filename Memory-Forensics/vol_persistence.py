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

# The specific registry key where malware loves to hide
TARGET_KEY = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"


def hunt_persistence():
    if not os.path.exists(VOL_PATH):
        print(f"[!] ERROR: Cannot find {VOL_PATH}")
        return

    print(f"[*] Analyzing: {MEMORY_FILE}")
    print(f"[*] Task: Hunting for Persistence in Registry Key:")
    print(f"    -> {TARGET_KEY}")
    print("=" * 90)

    # Command: vol.py -f <file> -r json windows.registry.printkey --key <TARGET_KEY>
    cmd = [
        sys.executable, VOL_PATH,
        "-f", MEMORY_FILE,
        "-r", "json",
        "windows.registry.printkey",
        "--key", TARGET_KEY
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print("[!] Volatility Failed:")
            print(result.stderr)
            return

        data = json.loads(result.stdout)

        if not data:
            print("[-] No entries found in this Run key, or the hive is paged out.")
            return

        print(f"{'REGISTRY HIVE':<30} | {'SUBKEY / VALUE NAME':<25} | {'DATA (THE PAYLOAD)'}")
        print("-" * 90)

        found_entries = False
        for entry in data:
            try:
                # Volatility 3 printkey output usually includes Hive Offset, Type, Name, and Data
                hive = str(entry.get('Hive Offset', 'Unknown'))
                name = str(entry.get('Name', ''))
                type_str = str(entry.get('Type', ''))
                data_val = str(entry.get('Data', ''))

                # We want to skip empty subkeys and focus on actual values (strings/paths)
                if name and data_val and "(empty)" not in data_val:
                    print(f"{hive:<30} | {name:<25} | {data_val}")
                    found_entries = True
            except Exception:
                continue

        if not found_entries:
            print("[-] No malicious payloads found in the Run keys.")

    except json.JSONDecodeError:
        print("[!] Error: Could not parse output. The plugin might have failed to read the Registry.")
    except Exception as e:
        print(f"[!] Unexpected Error: {e}")


if __name__ == '__main__':
    hunt_persistence()
