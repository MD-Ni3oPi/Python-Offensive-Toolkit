#!/usr/bin/env python3
import subprocess
import os
import sys

# ==========================================
# CONFIGURATION
# ==========================================
VOL_PATH = "./vol.py"
MEMORY_FILE = "/root/Desktop/Windows_Snapshot3.vmem"
TARGET_PID = 8936
YARA_FILE = "hunter.yar"


def create_yara_rule():
    # We write a YARA rule to look for common reverse shell indicators
    rule_content = """
    rule Python_Reverse_Shell {
        meta:
            description = "Hunts for reverse shell strings in Python memory"
            author = "Forensic Analyst"
        strings:
            $s1 = "cmd.exe" ascii wide nocase
            $s2 = "subprocess.Popen" ascii wide nocase
            $s3 = "socket.socket" ascii wide nocase
            $s4 = "os.system" ascii wide nocase
            $s5 = "pty.spawn" ascii wide nocase
        condition:
            any of them
    }
    """
    with open(YARA_FILE, "w") as f:
        f.write(rule_content)
    print(f"[*] Created YARA rule file: {YARA_FILE}")


def run_yara_scan():
    if not os.path.exists(VOL_PATH):
        print(f"[!] ERROR: Cannot find {VOL_PATH}")
        return

    print(f"[*] Analyzing: {MEMORY_FILE}")
    print(f"[*] Task: Scanning PID {TARGET_PID} memory with YARA rules...")
    print("=" * 90)

    # Command: vol.py -f file yarascan.YaraScan --yara-file hunter.yar
    cmd = [
        sys.executable, VOL_PATH,
        "-f", MEMORY_FILE,
        "yarascan.YaraScan",  # Changed plugin name
        # Removed the --pid flag entirely
        "--yara-file", YARA_FILE
    ]

    try:
        # We run this raw because YARA output is highly structured and looks great in terminal
        process = subprocess.run(cmd, capture_output=True, text=True)

        # Filter out the VMware warning if it pops up
        output_lines = process.stdout.split('\n')
        for line in output_lines:
            if "WARNING" not in line and "volatility3.framework" not in line:
                print(line)

        if process.stderr:
            err_lines = process.stderr.split('\n')
            for line in err_lines:
                if "WARNING" not in line and "volatility3.framework" not in line and line.strip() != "":
                    print(f"[!] {line}")

    except Exception as e:
        print(f"[!] Unexpected Error: {e}")


if __name__ == '__main__':
    create_yara_rule()
    run_yara_scan()

    # Clean up the yara file after we are done
    if os.path.exists(YARA_FILE):
        os.remove(YARA_FILE)
