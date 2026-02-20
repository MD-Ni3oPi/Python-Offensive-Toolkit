import socket  # Hint: The "Network Gateway." The standard library for all network communication.
import os  # Hint: The "System Scout." Used here to check if you are on Windows or Linux.

# host to listen on
HOST = '0.0.0.0'  # Hint: The "Ear." The specific IP address of your network card.


def main():
    # create raw socket, bind to public interface
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP  # Hint: "Windows Protocol." Windows requires this for raw IP.
    else:
        socket_protocol = socket.IPPROTO_TCP  # Hint: "Linux Protocol." Linux allows sniffing specific ICMP (pings)or TCP for (HTTP / HTTPS).

    # Hint: The "Raw Telescope." SOCK_RAW lets you see the packet headers, not just the data inside.
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

    # Hint: The "Anchor." Connects the sniffer to your specific IP address and any available port (0).
    sniffer.bind((HOST, 0))

    # include the ip header in the capture
    # Hint: "The Full Envelope." This tells the OS to give you the IP header (sender/receiver info) too.
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == 'nt':
        # Hint: "Eavesdropper Mode." This IOCTL command enables Promiscuous Mode on Windows.
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    # read one packet
    # Hint: "The Catcher." 65565 is the maximum size of a single IP packet it will grab.
    print(sniffer.recvfrom(65565))

    # if we are on windows , turn off promiscuous mode
    if os.name == 'nt':
        # Hint: "The Reset." Always turn off promiscuous mode so your network card returns to normal.
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == '__main__':
    main()
