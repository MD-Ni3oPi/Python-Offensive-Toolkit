# 🐍 Python Offensive Toolkit

## 📖 Overview
A curated collection of custom-built, Python-based offensive security tools designed for penetration testing, internal network assessments, and advanced CTF environments (Hack The Box, TryHackMe, CTFTime). 

When operating in restricted environments where standard binaries (like `nc`, `nmap`, or `wireshark`) are heavily monitored or entirely absent, these lightweight, pure-Python scripts allow an operator to "Bring Your Own Tools" (BYOT) to maintain access, pivot, and exfiltrate data.

## 🗂️ Toolkit Architecture

### 1. 🌐 Networking-Tools
Tools designed for raw network manipulation, port scanning without standard binaries, and persistent connection handling.
* **`netcat.py`:** A custom Netcat implementation for stealthy reverse shells and file transfers.
* **`TCP_Proxy.py`:** A bidirectional hexdump proxy for intercepting, analyzing, and modifying unknown or proprietary protocols on the fly.
* **`scanner.py`:** A stealthy UDP host discovery scanner using raw sockets—perfect for environments where `nmap` is unavailable.

### 2. 🔐 Custom-SSH (Command & Control)
Encrypted, stealthy communication channels utilizing the Paramiko library.
* **`SSH-Paramiko.py` / `SSH-rcmd.py`:** Custom SSH client and server scripts that establish encrypted reverse shells. These act as a lightweight, encrypted Command and Control (C2) channel that blends in with normal administrative traffic.

### 3. 🕵️ Network-Sniffing & MITM
Scripts built to analyze and exploit internal network traffic after gaining an initial foothold.
* **`MITM_Scrapper.py`:** ARP poisoning and Man-in-the-Middle utility to intercept plaintext credentials across a subnet.
* **`Mail-Sniffer.py`:** A targeted packet sniffer designed to extract POP3, IMAP, and SMTP authentication credentials from automated background tasks.
* **`detector.py`:** A defensive/offensive script to detect if ARP poisoning is actively occurring on the local network.

## 🎯 Strategic Value
This repository demonstrates a deep understanding of core network security engineering. Rather than solely relying on pre-built frameworks, these scripts showcase the ability to interact with raw sockets, manipulate packet payloads, and build custom encrypted channels from the ground up.

## ⚖️ Legal Disclaimer
**For Educational and Authorized Testing Purposes Only.** This toolkit is intended strictly for authorized penetration testing, incident response research, and controlled CTF environments. The author assumes no liability and is not responsible for any misuse or damage caused by these programs.
