import sys
import socket
import threading

# This filter converts non-printable characters into dots (.)
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])


def hexdump(src, length=16, show=True):
    # Ensure the input is in bytes format for processing
    if isinstance(src, bytes):
        src = src.decode(errors='replace')  # Decode bytes to string for translation

    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i + length])

        # Translate characters using our HEX_FILTER
        printable = word.translate(HEX_FILTER)

        # Convert each character to its 2-digit Hexadecimal representation
        hexa = ''.join([f'{ord(c):02X} ' for c in word])
        hexwidth = length * 3

        # Format the line: Offset | Hex Data | Printable Text
        results.append(f'{i:04x}  {hexa:<{hexwidth}}  {printable}')

    # This 'if' block must be OUTSIDE the 'for' loop to print once at the end
    if show:
        for line in results:
            print(line)
    else:
        return results


def receive_from(connection):
    # 1. Start with an empty byte buffer to store the incoming data
    buffer = b""

    # 2. Set a 5-second limit so the script doesn't wait forever
    connection.settimeout(5)

    try:
        while True:
            # 3. Read up to 4096 bytes from the socket
            data = connection.recv(4096)

            # 4. If no more data is arriving, break the loop
            if not data:
                break

            # 5. FIXED: Move this out of the 'if' block so data is actually saved!
            buffer += data

    except Exception as e:
        # 6. If the 5 seconds run out, just stop here and return what we have got
        pass

    return buffer

def request_handler(buffer):
    return buffer
    #perform packet modifications

def response_handler(buffer):
    return buffer
#perform packet modification
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    # Hint: Create the 'Outbound Phone' to talk to the real server
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Hint: 'Dial' the remote server's IP and Port
    remote_socket.connect((remote_host, remote_port))

    # Hint: Check if the server speaks first (like an FTP banner)
    if receive_first:
        # Hint: Listen for that initial greeting from the server
        remote_buffer = receive_from(remote_socket)
        # Hint: Show the raw greeting bytes on your screen
        hexdump(remote_buffer)

        # Hint: Run the greeting through the 'Editor' function
        remote_buffer = response_handler(remote_buffer)

        # Hint: If there is data to send, pass it to your local machine
        if len(remote_buffer):
            print("[<==] sending %d bytes to localhost." % len(remote_buffer))
            client_socket.send(remote_buffer)

    # Hint: The 'Conversation Loop' - keep data moving back and forth
    while True:
        # Hint: Catch any data sent from your local computer
        local_buffer = receive_from(client_socket)

        # Hint: If the local side sent something, process it
        if len(local_buffer):
            print("[==>] Received %d bytes from localhost." % len(local_buffer))
            # Hint: Show the local request in Hex format
            hexdump(local_buffer)

            # Hint: Apply any hacker modifications to the request
            local_buffer = request_handler(local_buffer)
            # Hint: Forward the (modified) request to the remote server
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        # Hint: Catch the response coming back from the remote server
        remote_buffer = receive_from(remote_socket)

        # Hint: If the server replied, process the response
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            # Hint: Show the server's response in Hex format
            hexdump(remote_buffer)

            # Hint: Apply any hacker modifications to the response
            remote_buffer = response_handler(remote_buffer)
            # Hint: Send the final result back to your local computer
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost.")

        # Hint: The 'Goodbye Check' - stop if one side stops talking
        if not len(local_buffer) or not len(remote_buffer):
            # Hint: Hang up the local connection
            client_socket.close()
            # Hint: Hang up the remote connection
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            # Hint: Break the loop and end this handler thread
            break

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    # Hint: Create the 'Front Door' socket for your local machine
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Hint: 'Reserve' the local port so your proxy can listen there
        server.bind((local_host, local_port))
    except Exception as e:
        # Hint: The 'Warning System' if the port is already being used
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host, local_port))

    # Hint: Put the socket in 'Listen' mode; allow 5 people in the queue
    server.listen(5)

    while True:
        # Hint: Pause here until a client actually connects to the proxy
        client_socket, addr = server.accept()

        # Hint: Print out information about the new local connection
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)

        # Hint: Create a 'Secretary' (Thread) to talk to the remote server
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first))

        # Hint: Start the thread so it runs in the background immediately
        proxy_thread.start()

def main():
    # Hint: 'sys.argv' is the "Argument List" that stores everything you typed in the terminal
    if len(sys.argv[1:]) != 5:
        # Hint: This is the "Instruction Manual" shown if you forget a flag
        print("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    # Hint: These lines "Unpack" your terminal text into variables the script can use
    local_host = sys.argv[1]
    local_port = int(sys.argv[2]) # Hint: 'int()' converts text numbers into real integers

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # Hint: This tells the proxy whether to wait for the server to speak first
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # Hint: Finally, "Press the Red Button" to start the server loop with your settings
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


# Hint: This is the "Engine Starter" that tells Python to run main() when the file is opened
if __name__ == '__main__':
    main()
