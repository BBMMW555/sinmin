# main.py
# -*- coding: utf-8 -*-

import os

from kivy.app import App
from kivy.core.window import Window
from kivy.utils import platform

from config import (APP_NAME, WINDOW_SIZE, DISCOVERY_PORT, MESSAGING_PORT,
                    BROADCAST_IP, BROADCAST_INTERVAL, USER_TIMEOUT)
from core.identity import Identity
from core.discovery import Discovery
from core.messaging import Messaging
from ui.main_screen import MainScreen


class MyChatApp(App):
    def build(self):
        self.title = APP_NAME

        # حجم النافذة على سطح المكتب فقط
        if WINDOW_SIZE is not None and platform in ("win", "linux", "macosx"):
            try:
                Window.size = WINDOW_SIZE
            except Exception:
                pass

        # مجلد آمن لحفظ الهوية على كل الأنظمة
        storage = os.path.join(self.user_data_dir, "identity.json")
        try:
            os.makedirs(self.user_data_dir, exist_ok=True)
        except Exception:
            pass

        identity  = Identity(storage_path=storage)
        discovery = Discovery(identity, DISCOVERY_PORT, MESSAGING_PORT,
                              BROADCAST_IP, BROADCAST_INTERVAL, USER_TIMEOUT)
        messaging = Messaging(MESSAGING_PORT)

        messaging.start()
        discovery.start()

        self.root_screen = MainScreen(identity, discovery, messaging)
        return self.root_screen

    def on_stop(self):
        try:
            self.root_screen.discovery.stop()
            self.root_screen.messaging.stop()
        except Exception:
            pass


if __name__ == "__main__":
    MyChatApp().run()