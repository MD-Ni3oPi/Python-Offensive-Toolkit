import ipaddress  # Hint: The "Subnet Calculator." Used to iterate through all IPs in the subnet.
import os  # Hint: The "System Scout." Checks if we are on Windows or Linux.
import socket  # Hint: The "Network Gateway." Essential for sending and receiving raw data.
import struct  # Hint: The "Binary Decoder." For parsing the returned ICMP responses.
import sys  # Hint: The "System Tailor." To handle command line arguments and exit cleanly.
import threading  # Hint: The "Multitasker." Allows sending UDP packets while sniffing simultaneously.
import time  # Hint: The "Clock." Used to give the sniffer a head start before sending.

# Define the target subnet and our secret "handshake" string
SUBNET = '192.168.72.0/24'
MESSAGE = 'PYTHONRULES!'


class ICMP:
    def __init__(self, buff):
        # Hint: 'BBH' maps to Type (1 byte), Code (1 byte), and Checksum (2 bytes).
        # This requires EXACTLY 4 bytes or it crashes the script.
        header = struct.unpack('<BBH', buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]


class IP:
    def __init__(self, buff=None):
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xF
        self.protocol_num = header[6]
        self.src = header[8]
        self.dst = header[9]
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception:
            self.protocol = str(self.protocol_num)


def udp_sender():
    # Hint: The "Broadcaster." Sprays UDP packets to trigger ICMP responses.
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sender.sendto(bytes(MESSAGE, 'utf8'), (str(ip), 65212))


class Scanner:
    def __init__(self, host):
        self.host = host
        socket_protocol = socket.IPPROTO_IP if os.name == 'nt' else socket.IPPROTO_ICMP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((host, 0))
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def sniff(self):
        hosts_up = {f'{str(self.host)} *'}
        print(f"[*] Starting sniffer on {self.host}...")
        try:
            while True:
                raw_buffer = self.socket.recvfrom(65535)[0]
                ip_header = IP(raw_buffer[0:20])

                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + 8]

                    # --- THE IRONCLAD GUARD ---
                    # This must be the ONLY way to reach the ICMP call.
                    if len(buf) >= 4:
                        icmp_header = ICMP(buf[:4])  # Only take the first 4 bytes

                        # Check for TYPE 3 and CODE 3
                        if icmp_header.code == 3 and icmp_header.type == 3:
                            if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(SUBNET):
                                # Verify magic message
                                if raw_buffer[len(raw_buffer) - len(MESSAGE):] == bytes(MESSAGE, 'utf8'):
                                    tgt = str(ip_header.src_address)
                                    if tgt != self.host and tgt not in hosts_up:
                                        hosts_up.add(tgt)
                                        print(f'Host Up: {tgt}')
        except KeyboardInterrupt:
            if os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            print('\nUser interrupted.')
            if hosts_up:
                print(f'\nSummary: Hosts up on {SUBNET}')
                for host in sorted(hosts_up):
                    print(f'{host}')
            sys.exit()


if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) == 2 else '0.0.0.0'
    s = Scanner(host)
    time.sleep(5)
    t = threading.Thread(target=udp_sender)
    t.start()
    s.sniff()
