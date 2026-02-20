# Hint: mitmproxy provides the 'http' flow which contains the decrypted data.
from mitmproxy import http
import os

# Hint: This is the same folder your detector.py looks at.
IMAGE_DIR = '/root/Desktop/pictures'

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)


def response(flow: http.HTTPFlow):
    # Hint: content-type tells us if the file is an image (jpg, png, etc.)
    content_type = flow.response.headers.get("Content-Type", "")

    if "image" in content_type:
        # Build a filename using the timestamp so they don't overwrite each other.
        ext = content_type.split("/")[-1]
        filename = f"img_{flow.request.timestamp_start}.{ext}"
        path = os.path.join(IMAGE_DIR, filename)

        # Hint: .content is the raw binary data of the image.
        with open(path, "wb") as f:
            f.write(flow.response.content)

        print(f"[*] Successfully saved: {filename}")
