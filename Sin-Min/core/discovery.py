# core/discovery.py
# -*- coding: utf-8 -*-

import socket
import threading
import json
import time


class Discovery:
    """اكتشاف الأجهزة على نفس شبكة الواي فاي عبر UDP Broadcast."""

    def __init__(self, identity, port, msg_port, broadcast_ip,
                 interval=2.0, timeout=10.0):
        self.identity = identity
        self.port = port
        self.msg_port = msg_port
        self.broadcast_ip = broadcast_ip
        self.interval = interval
        self.timeout = timeout
        self.peers = {}
        self._running = False
        self._lock = threading.Lock()
        self.on_peers_changed = None

    def _my_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"
        finally:
            s.close()

    def _broadcaster(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        except Exception:
            pass
        while self._running:
            try:
                payload = json.dumps({
                    "user_id": self.identity.user_id,
                    "nickname": self.identity.nickname,
                    "ip": self._my_ip(),
                    "msg_port": self.msg_port,
                })
                s.sendto(payload.encode("utf-8"),
                         (self.broadcast_ip, self.port))
            except Exception:
                pass
            time.sleep(self.interval)
        s.close()

    def _listener(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except Exception:
            pass
        try:
            s.bind(("", self.port))
        except Exception:
            # فشل الربط (منفذ مشغول) — لنبدأ الاستماع لاحقًا إن أمكن
            return
        s.settimeout(1.0)
        while self._running:
            try:
                data, addr = s.recvfrom(2048)
                info = json.loads(data.decode("utf-8"))
                if info.get("user_id") == self.identity.user_id:
                    continue
                info["ip"] = addr[0]
                info["last_seen"] = time.time()
                with self._lock:
                    self.peers[info["user_id"]] = info
                self._notify()
            except socket.timeout:
                self._cleanup()
            except Exception:
                pass
        s.close()

    def _cleanup(self):
        now = time.time()
        changed = False
        with self._lock:
            for uid in list(self.peers.keys()):
                if now - self.peers[uid]["last_seen"] > self.timeout:
                    del self.peers[uid]
                    changed = True
        if changed:
            self._notify()

    def _notify(self):
        if self.on_peers_changed:
            try:
                self.on_peers_changed(self.get_peers())
            except Exception:
                pass

    def get_peers(self):
        with self._lock:
            return list(self.peers.values())

    def start(self):
        if self._running:
            return
        self._running = True
        threading.Thread(target=self._broadcaster, daemon=True).start()
        threading.Thread(target=self._listener,    daemon=True).start()

    def stop(self):
        self._running = False