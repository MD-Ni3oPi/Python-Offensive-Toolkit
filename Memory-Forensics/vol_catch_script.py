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
PARENT_PID = 9952


def catch_the_script():
    if not os.path.exists(VOL_PATH):
        print(f"[!] ERROR: Cannot find {VOL_PATH}")
        return

    print(f"[*] Hunting for arguments on Parent PID: {PARENT_PID} (py.exe)")
    print("=" * 80)

    cmd = [sys.executable, VOL_PATH, "-f", MEMORY_FILE, "-r", "json", "windows.cmdline"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("[!] Volatility Failed:")
            print(result.stderr)
            return

        data = json.loads(result.stdout)

        print(f"{'PID':<6} | {'PROCESS':<15} | {'COMMAND LINE ARGS'}")
        print("-" * 80)

        found = False
        for entry in data:
            try:
                pid = entry.get('PID')
                process = str(entry.get('Process', ''))
                args = str(entry.get('Args', ''))

                # We specifically want to see PID 9952, or ANY process calling a .py file
                if pid == PARENT_PID or '.py' in args.lower() or 'py.exe' in process.lower():
                    print(f"{pid:<6} | {process:<15} | {args}")
                    found = True
            except Exception:
                continue

        if not found:
            print("[-] The parent process arguments are also gone from memory.")
            print("    The attacker might be running a fileless script (directly from RAM).")

    except Exception as e:
        print(f"[!] Unexpected Error: {e}")


if __name__ == '__main__':
    catch_the_script()
