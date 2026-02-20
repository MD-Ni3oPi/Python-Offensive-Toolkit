#!/usr/bin/env python3
import subprocess
import sys
import os

# ==========================================
# CONFIGURATION
# ==========================================
VOL_PATH = "./vol.py"
MEMORY_FILE = "/root/Desktop/Windows_Snapshot3.vmem"


def run_filescan():
    if not os.path.exists(VOL_PATH):
        print(f"[!] ERROR: Cannot find {VOL_PATH}")
        return

    print(f"[*] Analyzing: {MEMORY_FILE}")
    print("[*] Task: Deep scanning RAM for hidden/closed Python scripts...")
    print("    (This searches the entire 2GB file - please wait 1-3 minutes)")
    print("=" * 100)

    # Command: vol.py -f file windows.filescan
    cmd = [sys.executable, VOL_PATH, "-f", MEMORY_FILE, "windows.filescan"]

    try:
        # We process this line-by-line because the output is massive
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print(f"{'OFFSET (PHYSICAL)':<20} | {'FILE PATH'}")
        print("-" * 100)

        found = False
        for line in process.stdout:
            line_lower = line.lower()

            # SMART FILTER: We are looking for the smoking gun
            # 1. Any Python script (.py)
            # 2. Anything in the user's Downloads or Temp folders
            if ".py" in line_lower or "\\downloads\\" in line_lower or "\\temp\\" in line_lower:

                # Clean up the output formatting
                parts = line.split()
                if len(parts) >= 2:
                    offset = parts[0]
                    # Join the rest of the path back together (handles spaces in folder names)
                    file_path = " ".join(parts[1:])

                    # Ignore normal python library files to reduce noise
                    if "python3" not in line_lower and "site-packages" not in line_lower:
                        print(f"{offset:<20} | {file_path}")
                        found = True

        if not found:
            print("[-] No suspicious Python scripts or Downloads found in memory.")

    except Exception as e:
        print(f"[!] Unexpected Error: {e}")


if __name__ == '__main__':
    run_filescan()
