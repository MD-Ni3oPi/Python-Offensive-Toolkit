import asyncio
from aiosmtpd.controller import Controller

class DebugHandler:
    async def handle_DATA(self, server, session, envelope):
        print(f"\n[*] --- INCOMING EXFILTRATION ---")
        print(f"[*] From: {envelope.mail_from}")
        print(f"[*] To: {envelope.rcpt_tos}")
        print("[-] Encrypted Payload:")
        print(envelope.content.decode('utf8', errors='replace'))
        print("[*] -----------------------------")
        return '250 OK'

if __name__ == '__main__':
    controller = Controller(DebugHandler(), hostname='127.0.0.1', port=1025)
    controller.start()
    print("[*] SMTP Debug Server running on 127.0.0.1:1025...")
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        controller.stop()
