import paramiko
import getpass


def ssh_command(ip, port, user, passwd, cmd):
    # Hint: SSHClient is the "Remote Console" object that manages the connection.
    client = paramiko.SSHClient()

    # Hint: AutoAddPolicy is the "Trust Negotiator."
    # It automatically accepts the server's SSH key so the script doesn't hang.
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Hint: .connect() is the "Encrypted Doorway."
    # It performs the handshake and logs you in securely.
    client.connect(ip, port=port, username=user, password=passwd)

    # Hint: .exec_command() is the "Remote Arm."
    # It sends your command to the server and returns three streams: Input, Output, and Error.
    _, stdout, stderr = client.exec_command(cmd)

    output = stdout.readlines() + stderr.readlines()
    if output:
        print('--- Output ---')
        for line in output:
            print(line.strip())


if __name__ == '__main__':
    # Hint: getpass is for "Secret Typing."
    # It allows you to enter your password in the terminal without it appearing on the screen.
    user = input('Username: ')
    password = getpass.getpass()

    ip = input('Enter server IP: ') or '192.168.1.203'
    port = input('Enter port or <CR>: ') or 2222
    cmd = input('Enter command or <CR>: ') or 'id'

    ssh_command(ip, port, user, password, cmd)
