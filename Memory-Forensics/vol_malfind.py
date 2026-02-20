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
TARGET_PID = 8936


def run_malfind():
    if not os.path.exists(VOL_PATH):
        print(f"[!] ERROR: Cannot find {VOL_PATH}")
        return

    print(f"[*] Scanning PID {TARGET_PID} for injected code (Fileless Malware)...")
    print("=" * 90)

    # Command: vol.py -f file windows.malfind --pid 8936
    cmd = [sys.executable, VOL_PATH, "-f", MEMORY_FILE, "-r", "json", "windows.malfind", "--pid", str(TARGET_PID)]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("[!] Volatility Failed:")
            print(result.stderr)
            return

        data = json.loads(result.stdout)

        if not data:
            print("[-] Malfind did not detect any obvious injected memory regions.")
            print("    The attacker might have used advanced evasion (like module stomping).")
            return

        print(f"[+] MALICIOUS INJECTION DETECTED IN PID {TARGET_PID}!")
        print(f"{'START ADDRESS':<18} | {'END ADDRESS':<18} | {'PROTECTION':<25} | {'HEXDUMP PREVIEW'}")
        print("-" * 90)

        for entry in data:
            try:
                # Different Volatility 3 versions use slightly different keys for Start/End
                start = str(entry.get('Start VPN', entry.get('Start', 'N/A')))
                end = str(entry.get('End VPN', entry.get('End', 'N/A')))
                protection = str(entry.get('Protection', 'N/A'))

                # We pull the first 16 characters of the hex dump as a preview
                hexdump_raw = entry.get('Hexdump', '')
                hex_preview = str(hexdump_raw)[:20].replace('\n', ' ') + "..." if hexdump_raw else "N/A"

                print(f"{start:<18} | {end:<18} | {protection:<25} | {hex_preview}")
            except Exception:
                continue

        print("=" * 90)
        print("[*] Note: If the protection is 'PAGE_EXECUTE_READWRITE', you found the payload!")

    except json.JSONDecodeError:
        print("[!] Error: Could not parse output. Plugin might have failed.")
    except Exception as e:
        print(f"[!] Unexpected Error: {e}")


if __name__ == '__main__':
    run_malfind()
