#!/usr/bin/env python3
import argparse
import sys
from scapy.all import rdpcap, TCP, Raw

def extract_ftp_creds(pcap_path):
    print(f"[*] Loading PCAP file: {pcap_path}")
    try:
        # Load the packet capture into memory
        packets = rdpcap(pcap_path)
    except FileNotFoundError:
        print(f"[-] Error: PCAP file '{pcap_path}' not found.")
        sys.exit(1)

    print("[*] Hunting for cleartext FTP credentials...")
    for packet in packets:
        # Check if the packet contains both a TCP layer and a Raw data payload
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            # Port 21 is the FTP control channel
            if packet[TCP].dport == 21 or packet[TCP].sport == 21:
                try:
                    payload = packet[Raw].load.decode('utf-8', errors='ignore').strip()
                    if "USER" in payload or "PASS" in payload or "Login successful" in payload:
                        print(f"[+] {payload}")
                except Exception:
                    pass

if __name__ == "__main__":
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Extract cleartext FTP credentials from a PCAP file.")
    
    # Define the expected command-line argument
    parser.add_argument("pcap_file", help="Path to the target PCAP file")
    
    # Parse the input provided by the user
    args = parser.parse_args()
    
    # Run the function using the dynamic argument
    extract_ftp_creds(args.pcap_file)
