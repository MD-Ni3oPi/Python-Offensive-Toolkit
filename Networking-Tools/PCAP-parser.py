#!/usr/bin/env python3
import sys
from scapy.all import rdpcap, TCP, Raw

def extract_ftp_creds(pcap_path):
    print(f"[*] Loading PCAP file: {pcap_path}")
    try:
        # Load the packet capture into memory
        packets = rdpcap(pcap_path)
    except FileNotFoundError:
        print("[-] Error: PCAP file not found.")
        return

    print("[*] Hunting for cleartext FTP credentials...")
    
    # Iterate through every packet in the capture
    for packet in packets:
        # Check if the packet contains both a TCP layer and a Raw data payload
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            # Filter for FTP traffic (Port 21 is the control channel)
            if packet[TCP].dport == 21 or packet[TCP].sport == 21:
                try:
                    # Extract the payload and decode it from bytes to string
                    payload = packet[Raw].load.decode('utf-8', errors='ignore').strip()
                    
                    # Search for authentication keywords
                    if "USER" in payload or "PASS" in payload or "Login successful" in payload:
                        print(f"[+] {payload}")
                except Exception as e:
                    pass # Ignore decoding errors on non-text payloads

if __name__ == "__main__":
    # Point this to the file you downloaded from the Cap machine
    target_pcap = "1 (1).pcap" 
    extract_ftp_creds(target_pcap)
