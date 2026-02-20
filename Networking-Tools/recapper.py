from scapy.all import TCP, rdpcap  # Hint: rdpcap is the "PCAP Reader" that loads your saved capture into Python.
import collections
import os  # Hint: The "File Manager" used to create folders and join file paths.
import re  # Hint: The "Text Pattern Matcher" (Regular Expressions) used to parse HTTP headers.
import sys
import zlib  # Hint: The "Decompressor" used to unpack images that were zipped during transfer (GZIP/Deflate).

# Update these paths to match your Kali setup
OUTDIR = '/root/Desktop/pictures'  # Hint: The "Photo Album" folder where extracted images will be saved.
PCAPS = '/root/PyCharmMiscProject'  # Hint: The "Storage Room" where your pcap file is located.

Response = collections.namedtuple('Response', ['header', 'payload'])


def get_header(payload):
    try:
        # Hint: Splits the raw data to find where the HTTP header ends and the image begins.
        header_raw = payload[:payload.index(b'\r\n\r\n') + 2]
    except ValueError:
        sys.stdout.write('-')
        sys.stdout.flush()
        return None

    # Hint: Uses Regex to turn raw header text into a searchable Python Dictionary.
    header = dict(re.findall(r'(?P<name>.*?): (?P<value>.*?)\r\n', header_raw.decode()))
    if 'Content-Type' not in header:
        return None
    return header


def extract_content(Response, content_name='image'):
    content, content_type = None, None
    if content_name in Response.header['Content-Type']:
        content_type = Response.header['Content-Type'].split('/')[1]
        content = Response.payload[Response.payload.index(b'\r\n\r\n') + 4:]

        # Hint: Handles compressed data to ensure the image isn't "broken."
        if 'Content-Encoding' in Response.header:
            if Response.header['Content-Encoding'] == "gzip":
                content = zlib.decompress(content, zlib.MAX_WBITS | 32)
            elif Response.header['Content-Encoding'] == "deflate":
                content = zlib.decompress(content)
    return content, content_type


class Recapper:
    def __init__(self, fname):
        pcap = rdpcap(fname)
        # Hint: A powerful Scapy feature that automatically groups packets into "Conversations."
        self.sessions = pcap.sessions()
        self.responses = list()

    def get_responses(self):
        for session in self.sessions:
            payload = b''
            for packet in self.sessions[session]:
                try:
                    # Hint: Filters for web traffic (Port 80).
                    if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                        payload += bytes(packet[TCP].payload)
                except IndexError:
                    sys.stdout.write('x')
                    sys.stdout.flush()

            if payload:
                header = get_header(payload)
                if header is not None:
                    self.responses.append(Response(header=header, payload=payload))

    def write(self, content_name):
        for i, response in enumerate(self.responses):
            content, content_type = extract_content(response, content_name)
            if content and content_type:
                fname = os.path.join(OUTDIR, f'ex_{i}.{content_type}')
                print(f'Writing {fname}')
                with open(fname, 'wb') as f:
                    f.write(content)


if __name__ == '__main__':
    pfile = os.path.join(PCAPS, 'arper.pcap')  # Hint: Ensure your capture is named 'pcap.pcap'.
    recapper = Recapper(pfile)
    recapper.get_responses()
    recapper.write('image')
