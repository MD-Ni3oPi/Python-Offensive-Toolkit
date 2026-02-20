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


def trace_lineage():
    if not os.path.exists(VOL_PATH):
        print(f"[!] ERROR: Cannot find {VOL_PATH}")
        return

    print(f"[*] Tracing Execution Lineage for PID: {TARGET_PID}")
    print("=" * 60)

    # We run pslist to get the full list of processes and their parents
    cmd = [sys.executable, VOL_PATH, "-f", MEMORY_FILE, "-r", "json", "windows.pslist"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("[!] Volatility Failed:")
            return

        data = json.loads(result.stdout)

        # 1. Find our target
        target_process = None
        for entry in data:
            if entry.get('PID') == TARGET_PID:
                target_process = entry
                break

        if not target_process:
            print("[-] Target PID not found in pslist. It might be deeply hidden.")
            return

        # 2. Extract its Parent PID (PPID)
        ppid = target_process.get('PPID')
        print(f"[+] TARGET FOUND: python.exe (PID: {TARGET_PID})")
        print(f"    └── Spawned by Parent PID: {ppid}")
        print("-" * 60)

        # 3. Find the Parent Process
        parent_process = None
        for entry in data:
            if entry.get('PID') == ppid:
                parent_process = entry
                break

        if parent_process:
            p_name = parent_process.get('ImageFileName', 'Unknown')
            p_pid = parent_process.get('PID')
            p_ppid = parent_process.get('PPID')
            print(f"[+] PARENT FOUND: {p_name} (PID: {p_pid})")

            # 4. Find the Grandparent (just to be thorough)
            for entry in data:
                if entry.get('PID') == p_ppid:
                    gp_name = entry.get('ImageFileName', 'Unknown')
                    print(f"    └── Spawned by Grandparent: {gp_name} (PID: {p_ppid})")
                    break
        else:
            print(f"[-] Parent PID {ppid} is dead/missing. (Attacker likely closed the terminal).")

    except Exception as e:
        print(f"[!] Error: {e}")


if __name__ == '__main__':
    trace_lineage()
