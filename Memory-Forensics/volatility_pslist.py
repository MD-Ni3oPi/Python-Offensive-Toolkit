#!/usr/bin/env python3
import subprocess
import json
import sys
import os

# ==========================================
# CONFIGURATION
# ==========================================
# The exact command that worked manually, but we add '-r json' to make it computer-readable
VOL_PATH = "./vol.py"
MEMORY_FILE = "/root/Desktop/Windows_Snapshot3.vmem"
PLUGIN = "windows.pslist"


def run_volatility_wrapper():
    # 1. Check if vol.py exists
    if not os.path.exists(VOL_PATH):
        print(f"[!] ERROR: Cannot find {VOL_PATH}")
        print("    Are you in the 'volatility3' folder?")
        return

    # 2. Construct the Command
    # python3 vol.py -f <file> -r json windows.pslist
    cmd = [
        sys.executable,  # Uses the current python3 interpreter
        VOL_PATH,
        "-f", MEMORY_FILE,
        "-r", "json",  # Request JSON output (easier to parse)
        PLUGIN
    ]

    print(f"[*] Running command: {' '.join(cmd)}")
    print("[*] Analysis Started... (This keeps the Automagic intact!)")

    try:
        # 3. Execute and Capture Output
        # This runs the tool exactly like you did manually, but captures the text
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        # 4. Check for Errors
        if result.returncode != 0:
            print("[!] Volatility Failed:")
            print(result.stderr)
            return

        # 5. Parse the JSON Data
        # The output comes back as a big string; we turn it into a Python List
        data = json.loads(result.stdout)

        print("\n[+] Success! Parsed Process List:")
        print("=" * 60)
        print(f"{'PID':<10} | {'PPID':<10} | {'IMAGE NAME'}")
        print("=" * 60)

        # 6. Loop through the data
        # JSON output structure is usually a list of dictionaries
        for entry in data:
            try:
                # We fetch fields by name (safer than index!)
                pid = entry.get('PID', 'N/A')
                ppid = entry.get('PPID', 'N/A')
                name = entry.get('ImageFileName', 'N/A')

                print(f"{str(pid):<10} | {str(ppid):<10} | {str(name)}")
            except AttributeError:
                continue

    except json.JSONDecodeError:
        print("[!] Error: Could not parse JSON output.")
        print("Raw Output:", result.stdout)
    except Exception as e:
        print(f"[!] Unexpected Error: {e}")


if __name__ == '__main__':
    run_volatility_wrapper()
