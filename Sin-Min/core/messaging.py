# core/messaging.py
# -*- coding: utf-8 -*-

import socket
import threading


class Messaging:
    """إرسال/استقبال نصي مباشر عبر TCP."""

    def __init__(self, port):
        self.port = port
        self._running = False
        self.on_message = None  # callback(sender_ip, text)

    def send(self, target_ip, target_port, text):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3.0)
                s.connect((target_ip, target_port))
                s.sendall(text.encode("utf-8"))
            return True
        except Exception as e:
            print(f"[messaging] send error: {e}")
            return False

    def _server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except Exception:
            pass
        try:
            s.bind(("", self.port))
        except Exception:
            return
        s.listen(5)
        s.settimeout(1.0)
        while self._running:
            try:
                conn, addr = s.accept()
                data = conn.recv(8192).decode("utf-8")
                if data and self.on_message:
                    try:
                        self.on_message(addr[0], data)
                    except Exception:
                        pass
                conn.close()
            except socket.timeout:
                continue
            except Exception:
                pass
        s.close()

    def start(self):
        if self._running:
            return
        self._running = True
        threading.Thread(target=self._server, daemon=True).start()

    def stop(self):
        self._running = False