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
TARGET_PID = 8936  # The suspicious Python process we found


def run_pid_recon():
    if not os.path.exists(VOL_PATH):
        print(f"[!] ERROR: Cannot find {VOL_PATH}")
        return

    print(f"[*] Investigating Suspicious PID: {TARGET_PID}")
    print("=" * 60)

    # 1. Run 'windows.cmdline' to see the script path
    print("[*] Phase 1: Extracting Command Line Arguments...")
    cmd = [sys.executable, VOL_PATH, "-f", MEMORY_FILE, "-r", "json", "windows.cmdline"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)

        found = False
        for entry in data:
            if entry.get('PID') == TARGET_PID:
                print(f"[+] FOUND COMMAND LINE:")
                print(f"    Process: {entry.get('Process')}")
                print(f"    Args:    {entry.get('Args')}")
                found = True
                break

        if not found:
            print("[-] PID not found in command line history (Process might have exited).")

    except Exception as e:
        print(f"[!] Error reading cmdline: {e}")

    print("-" * 60)

    # 2. Run 'windows.ldrmodules' to see where the executable launched from
    print("[*] Phase 2: Verifying Binary Path (dlllist)...")
    cmd = [sys.executable, VOL_PATH, "-f", MEMORY_FILE, "-r", "json", "windows.dlllist", "--pid", str(TARGET_PID)]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)

        # The first entry in dlllist is usually the binary itself
        if data:
            binary = data[0].get('Path', 'Unknown')
            cmdline = data[0].get('CommandLine', 'Unknown')
            print(f"[+] BINARY PATH: {binary}")
            if not found:  # Fallback if cmdline plugin failed
                print(f"[+] ARGS (from dlllist): {cmdline}")
        else:
            print("[-] No DLL data found for this PID.")

    except Exception as e:
        print(f"[!] Error reading dlllist: {e}")


if __name__ == '__main__':
    run_pid_recon()
