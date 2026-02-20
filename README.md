# 🐍 Python Offensive & DFIR Toolkit

## 📖 Overview
A comprehensive, custom-built Python framework designed for advanced penetration testing, Red/Purple Team operations, and high-level CTF environments (Hack The Box, TryHackMe, CTFTime). 

This repository demonstrates the ability to bypass restricted environments by utilizing "Bring Your Own Tools" (BYOT) methodologies. It covers the entire attack lifecycle: from raw network manipulation and stealthy Command & Control (C2), to Windows privilege escalation, data exfiltration, and finally, memory forensics to hunt the very malware deployed.

## 🗂️ Toolkit Architecture

### 1. 🌐 Networking-Tools (Initial Access & Pivoting)
Tools designed for raw network manipulation and persistent connection handling when standard binaries (`nc`, `nmap`) are unavailable.
* **`netcat.py`:** A custom pure-Python Netcat clone for reverse shells and file transfers.
* **`TCP_Proxy.py`:** A bidirectional hexdump proxy for intercepting and modifying proprietary protocols.
* **`scanner.py`:** A stealthy UDP host discovery scanner using raw sockets.

### 2. 🔐 Custom-SSH (Command & Control)
Encrypted, stealthy communication channels utilizing the Paramiko library.
* **`SSH-Paramiko.py` & `SSH-rcmd.py`:** Custom SSH client/server scripts that establish encrypted reverse shells, acting as a lightweight C2 channel that blends with administrative traffic.

### 3. 🧟 GitHub-C2-Trojan (Advanced Persistence)
An advanced Red Team module that uses the GitHub API as a legitimate, highly trusted C2 infrastructure to bypass network-based IDS.
* **`trojan.py`:** The core implant that pulls commands from and pushes data to a GitHub repository.
* **`c2_github.py` & `git_test.py`:** Handler scripts for API interfacing and deployment testing.
* **`decrypt.py`:** Utility to decode the exfiltrated, encrypted payload chunks.

### 4. 🕵️ Network-Sniffing & MITM (Interception)
Scripts built to analyze and exploit internal network traffic after gaining a foothold.
* **`MITM_Scrapper.py`:** ARP poisoning utility to intercept plaintext credentials.
* **`Mail-Sniffer.py`:** Packet sniffer designed to extract POP3, IMAP, and SMTP credentials.
* **`detector.py`:** A script to detect active ARP poisoning on the local network.

### 5. 🪟 Windows-Post-Exploitation (Privilege Escalation)
Scripts designed to interact with Windows Internals and WMI for lateral movement and privilege escalation.
* **`process_monitor.py` & `file_monitor.py`:** WMI monitors that track high-privileged background tasks to exploit temporary files and processes.
* **`token_stealler.py`:** Advanced script to duplicate and impersonate highly privileged access tokens (e.g., `NT AUTHORITY\SYSTEM`).

### 6. 📤 Data-Exfiltration (DLP Evasion)
Post-exploitation scripts designed to smuggle data out of restricted networks while evading Data Loss Prevention (DLP) systems.
* **`cryptor.py` & `decrypto_loot.py`:** Custom payload encryption/decryption.
* **`http_exfil.py`, `https_exfil.py`, `email_exfil.py`:** Protocol-specific smugglers to blend malicious transfers into normal web/mail traffic.
* **`auto_thif.py` & `recursive_thif.py`:** Automated file discovery and staging.
* **`Burp_exfil.py`:** Custom Burp Suite extension for manipulating web traffic exfiltration.

### 7. 🧠 Memory-Forensics (DFIR & Blue Team)
A massive suite of automated Volatility 3 scripts proving an understanding of how to hunt the techniques utilized above.
* **Process & Injection Hunting:** `vol_malfind.py`, `vol_pid_recon.py`, `volatility_pslist.py`, `vol_parent.py`
* **Network & Persistence:** `vol_network.py`, `vol_persistence.py`, `vol_servicess.py`
* **Extraction & Scanning:** `vol_dump_malware.py`,
