import getpass
import os
import socket
import select
import sys
import threading
import optparse  # Hint: Library for terminal flags like -p and -u.
import paramiko  # Hint: The core SSH engine for the connection.


# Hint: This function handles the status messages seen in the book's output.
def verbose(s):
    print(s)


# Hint: This function allows main() to "unpack" the 3 variables it needs.
def parse_options():
    parser = optparse.OptionParser()
    parser.add_option('-p', '--remote-port', type='int', dest='port', default=80)
    parser.add_option('-u', '--user', dest='user', default='root')
    parser.add_option('-K', '--key', dest='keyfile', default=None)
    parser.add_option('-P', '--password', action='store_true', dest='readpass', default=False)

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error('Incorrect number of arguments.')

    # Hint: Splits the input (e.g., 127.0.0.1:22) into a host and port.
    temp_server = args[0].split(':')
    server = (temp_server[0], int(temp_server[1]))
    remote = ('127.0.0.1', options.port)
    return options, server, remote


# Hint: The "Middleman" function that moves data between SSH and the local port.
def handler(chan, host, port):
    sock = socket.socket()  # Hint: Creates a network socket.
    try:
        sock.connect((host, port))  # Hint: Connects to the local web server.
    except Exception as e:
        verbose('Forwarding request to %s:%d failed: %r' % (host, port, e))
        return

    verbose('Connected! Tunnel open %r -> %r -> %r' % (chan.origin_addr, chan.getpeername(), (host, port)))

    while True:
        # Hint: 'select' watches both sides for data so the script doesn't freeze.
        r, w, x = select.select([sock, chan], [], [])
        if sock in r:
            data = sock.recv(1024)
            if len(data) == 0: break
            chan.send(data)
        if chan in r:
            data = chan.recv(1024)
            if len(data) == 0: break
            sock.send(data)

    chan.close()
    sock.close()
    verbose('Tunnel closed from %r' % (chan.origin_addr,))


# Hint: Tells the remote SSH server to open a port and wait for traffic.
def reverse_forward_tunnel(server_port, remote_host, remote_port, transport):
    # Hint: This is the specific request to the SSH server to start forwarding.
    transport.request_port_forward('', server_port)
    while True:
        chan = transport.accept(1000)  # Hint: Waits for someone to connect to the port.
        if chan is None:
            continue
        # Hint: Uses 'threading' to handle multiple connections at once.
        thr = threading.Thread(target=handler, args=(chan, remote_host, remote_port))
        thr.setDaemon(True)
        thr.start()


def main():
    options, server, remote = parse_options()
    password = None
    if options.readpass:
        password = getpass.getpass('Enter SSH password: ')  # Hint: Hides password entry.

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    verbose('Connecting to ssh host %s:%d ...' % (server[0], server[1]))
    try:
        # Hint: Connects using the username and password/key provided.
        client.connect(server[0], server[1], username=options.user,
                       key_filename=options.keyfile, password=password)
    except Exception as e:
        print('*** Failed to connect to %s:%d: %r' % (server[0], server[1], e))
        sys.exit(1)

    verbose('Now forwarding remote port %d to %s:%d ...' % (options.port, remote[0], remote[1]))

    try:
        # Hint: Starts the reverse tunnel logic using the connection's transport layer.
        reverse_forward_tunnel(options.port, remote[0], remote[1], client.get_transport())
    except KeyboardInterrupt:
        print('C-c: Port forwarding stopped.')
        sys.exit(0)


# Hint: This is the "Ignition Switch" that actually runs the code.
if __name__ == '__main__':
    main()
