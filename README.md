# 🐍 Python Offensive Toolkit

## 📖 Overview
A curated collection of custom-built, Python-based offensive security tools designed for penetration testing, internal network assessments, and advanced CTF environments (Hack The Box, TryHackMe, CTFTime). 

When operating in restricted environments where standard binaries (like `nc`, `nmap`, or `wireshark`) are heavily monitored or entirely absent, these lightweight, pure-Python scripts allow an operator to "Bring Your Own Tools" (BYOT) to maintain access, pivot, and exfiltrate data.

## 🗂️ Toolkit Architecture

### 1. 🌐 Networking-Tools
Tools designed for raw network manipulation, port scanning without standard binaries, and persistent connection handling.
* **`netcat.py`:** A custom Netcat implementation for stealthy reverse shells and file transfers.
* **`TCP_Proxy.py`:** A bidirectional hexdump proxy for intercepting, analyzing, and modifying unknown or proprietary protocols on the fly.
* **`scanner.py`:** A stealthy UDP host discovery scanner using raw sockets.

### 2. 🔐 Custom-SSH (Command & Control)
Encrypted, stealthy communication channels utilizing the Paramiko library.
* **`SSH-Paramiko.py` / `SSH-rcmd.py`:** Custom SSH client and server scripts that establish encrypted reverse shells, acting as a lightweight C2 channel.

### 3. 🕵️ Network-Sniffing & MITM
Scripts built to analyze and exploit internal network traffic.
* **`MITM_Scrapper.py`:** ARP poisoning and Man-in-the-Middle utility to intercept plaintext credentials.
* **`Mail-Sniffer.py`:** A targeted packet sniffer designed to extract POP3, IMAP, and SMTP authentication credentials.
* **`detector.py`:** A defensive/offensive script to detect active ARP poisoning on the local network.

### 4. 📤 Data-Exfiltration
Advanced post-exploitation scripts designed to smuggle data out of restricted networks while evading Data Loss Prevention (DLP) and Intrusion Detection Systems (IDS).
* **`auto_thif.py` & `recursive_thif.py`:** Automated file discovery and staging tools.
* **`cryptor.py` & `decrypto_loot.py`:** Custom payload encryption/decryption to obscure stolen data in transit.
* **`http_exfil.py`, `https_exfil.py`, `email_exfil.py`:** Protocol-specific exfiltration scripts to blend malicious data transfers in with normal web and mail traffic.
* **`Burp_exfil.py`:** A custom Burp Suite extension script for manipulating web traffic exfiltration.
* **`Packetsniff-win-linx.py`:** Cross-platform packet sniffing for targeted data capture.

## 🎯 Strategic Value
This repository demonstrates a deep understanding of core network security engineering and Red Team tradecraft. Rather than solely relying on pre-built frameworks, these scripts showcase the ability to interact with raw sockets, build custom encrypted channels, and stealthily exfiltrate data from the ground up.

## ⚖️ Legal Disclaimer
**For Educational and Authorized Testing Purposes Only.** This toolkit is intended strictly for authorized penetration testing, incident response research, and controlled CTF environments. The author assumes no liability and is not responsible for any misuse or damage caused by these programs.
