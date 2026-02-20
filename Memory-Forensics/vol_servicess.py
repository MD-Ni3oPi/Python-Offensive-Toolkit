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
PLUGIN = "windows.svcscan"


def hunt_services():
    if not os.path.exists(VOL_PATH):
        print(f"[!] ERROR: Cannot find {VOL_PATH}")
        return

    print(f"[*] Analyzing: {MEMORY_FILE}")
    print("[*] Task: Scanning for Malicious Windows Services...")
    print("=" * 110)

    # Command: vol.py -f <file> -r json windows.svcscan
    cmd = [sys.executable, VOL_PATH, "-f", MEMORY_FILE, "-r", "json", PLUGIN]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print("[!] Volatility Failed:")
            print(result.stderr)
            return

        data = json.loads(result.stdout)

        print(f"{'PID':<6} | {'STATE':<10} | {'SERVICE NAME':<20} | {'BINARY PATH (PAYLOAD)'}")
        print("-" * 110)

        found_suspicious = False
        for entry in data:
            try:
                pid = str(entry.get('PID', 'N/A'))
                state = str(entry.get('State', 'Unknown'))
                name = str(entry.get('Name', 'Unknown'))
                path = str(entry.get('Binary', 'Unknown'))

                path_lower = path.lower()

                # SMART FILTER: Hide normal Windows system services to reduce noise
                # If it is in System32 or SysWOW64, we ignore it UNLESS it runs a script
                if "system32" in path_lower or "syswow64" in path_lower:
                    suspicious_keywords = ['python', 'powershell', 'cmd.exe', '.bat', '.vbs', '.ps1']
                    if not any(keyword in path_lower for keyword in suspicious_keywords):
                        continue  # Skip normal system files

                # Also skip empty/driver paths
                if not path or path == "Unknown" or path_lower.startswith(r"\systemroot\system32\drivers"):
                    continue

                print(f"{pid:<6} | {state:<10} | {name:<20} | {path}")
                found_suspicious = True

            except Exception:
                continue

        if not found_suspicious:
            print("[-] No obviously suspicious services found outside of System32.")

    except json.JSONDecodeError:
        print("[!] Error: Could not parse output. Plugin might have failed.")
    except Exception as e:
        print(f"[!] Unexpected Error: {e}")


if __name__ == '__main__':
    hunt_services()
