#!/usr/bin/env python3
import subprocess
import sys
import os

# ==========================================
# CONFIGURATION
# ==========================================
VOL_PATH = "./vol.py"
MEMORY_FILE = "/root/Desktop/Windows_Snapshot3.vmem"

# The physical offsets we found in the filescan
TARGET_OFFSETS = [
    "0x9b04b3b23540",  # _native.cp314-win_amd64.pyd
    "0x9b04b3b27550"  # manage.cp314-win_amd64.pyd
]

DUMP_DIR = "./dumped_files"


def extract_files():
    if not os.path.exists(VOL_PATH):
        print(f"[!] ERROR: Cannot find {VOL_PATH}")
        return

    if not os.path.exists(DUMP_DIR):
        os.makedirs(DUMP_DIR)
        print(f"[*] Created output directory: {DUMP_DIR}")

    print(f"[*] Analyzing: {MEMORY_FILE}")
    print("[*] Task: Extracting PyManager payload files from memory...")
    print("=" * 80)

    for offset in TARGET_OFFSETS:
        print(f"[*] Attempting to dump file at physical offset {offset}...")

        # Command: vol.py -f <file> -o <dir> windows.dumpfiles --physaddr <offset>
        cmd = [
            sys.executable, VOL_PATH,
            "-f", MEMORY_FILE,
            "-o", DUMP_DIR,
            "windows.dumpfiles",
            "--physaddr", offset
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)

            output_lines = result.stdout.split('\n') + result.stderr.split('\n')
            found = False
            for line in output_lines:
                if "Data written to" in line or "file." in line:
                    filename = line.strip().split()[-1]
                    print(f"[+] SUCCESS: Extracted file saved as {filename}")
                    found = True

            if not found:
                print(f"[-] WARNING: Could not extract file at {offset}. It may be paged out or corrupted.")

        except Exception as e:
            print(f"[!] Error extracting {offset}: {e}")

    print("=" * 80)
    print(f"[*] Extraction complete. Check the '{DUMP_DIR}' folder for the output files.")


if __name__ == '__main__':
    extract_files()
