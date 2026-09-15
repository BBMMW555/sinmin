# ui/main_screen.py
# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp


class MainScreen(BoxLayout):
    """الواجهة الرئيسية: شريط علوي + منطقة محادثة + لوحة جانبية قابلة للطي."""

    SIDE_WIDTH = dp(220)

    def __init__(self, identity, discovery, messaging, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.identity = identity
        self.discovery = discovery
        self.messaging = messaging
        self.current_target = None
        self._build_ui()
        self._wire_backend()

    # ---------- UI ----------
    def _build_ui(self):
        top = BoxLayout(size_hint_y=None, height=dp(50),
                        padding=dp(4), spacing=dp(4))
        self.title_lbl = Label(
            text=f"Sin-Min | {self.identity.nickname} ({self.identity.user_id})",
            halign="left", valign="middle"
        )
        self.title_lbl.bind(
            size=lambda *a: setattr(self.title_lbl, "text_size", self.title_lbl.size)
        )
        btn_refresh = Button(text="Refresh", size_hint_x=None, width=dp(80),
                             on_press=self.on_refresh)
        btn_toggle = Button(text="Users", size_hint_x=None, width=dp(70),
                            on_press=self.toggle_side_panel)
        top.add_widget(self.title_lbl)
        top.add_widget(btn_refresh)
        top.add_widget(btn_toggle)
        self.add_widget(top)

        body = BoxLayout(orientation="horizontal")
        self.chat_area = self._build_chat_area()
        self.side_panel = self._build_side_panel()
        self.side_panel.size_hint_x = None
        self.side_panel.width = 0
        self.side_panel.opacity = 0
        body.add_widget(self.chat_area)
        body.add_widget(self.side_panel)
        self.add_widget(body)

    def _build_chat_area(self):
        layout = BoxLayout(orientation="vertical", padding=dp(6), spacing=dp(6))
        self.target_lbl = Label(text="No target selected",
                                size_hint_y=None, height=dp(28))
        layout.add_widget(self.target_lbl)

        scroll = ScrollView()
        self.chat_display = TextInput(readonly=True, multiline=True)
        scroll.add_widget(self.chat_display)
        layout.add_widget(scroll)

        bottom = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(4))
        self.msg_input = TextInput(hint_text="Type message...", multiline=False)
        self.msg_input.bind(on_text_validate=self.on_send)
        btn_send = Button(text="Send", size_hint_x=None, width=dp(80),
                          on_press=self.on_send)
        bottom.add_widget(self.msg_input)
        bottom.add_widget(btn_send)
        layout.add_widget(bottom)
        return layout

    def _build_side_panel(self):
        layout = BoxLayout(orientation="vertical", padding=dp(6), spacing=dp(6))

        icons = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(4))
        self.btn_wifi = Button(text="WiFi: ON", on_press=self.toggle_wifi)
        self.btn_bt = Button(text="BT: soon", on_press=self.toggle_bt)
        icons.add_widget(self.btn_wifi)
        icons.add_widget(self.btn_bt)
        layout.add_widget(icons)

        layout.add_widget(Label(text="Users online:",
                                size_hint_y=None, height=dp(26)))

        scroll = ScrollView()
        self.users_box = BoxLayout(orientation="vertical",
                                   size_hint_y=None, spacing=dp(2))
        self.users_box.bind(minimum_height=self.users_box.setter("height"))
        scroll.add_widget(self.users_box)
        layout.add_widget(scroll)
        return layout

    # ---------- ربط الواجهة بالمنطق ----------
    def _wire_backend(self):
        self.discovery.on_peers_changed = self._on_peers_changed
        self.messaging.on_message = self._on_message

    def _on_peers_changed(self, peers):
        Clock.schedule_once(lambda dt: self._refresh_user_list(peers))

    def _on_message(self, sender_ip, text):
        Clock.schedule_once(lambda dt: self._append_chat(f"[{sender_ip}] {text}"))

    def _refresh_user_list(self, peers):
        self.users_box.clear_widgets()
        for p in peers:
            btn = Button(text=f"{p['nickname']} ({p['user_id']})",
                         size_hint_y=None, height=dp(36))
            btn.bind(on_press=lambda inst, peer=p: self.select_target(peer))
            self.users_box.add_widget(btn)

    # ---------- الأحداث ----------
    def on_refresh(self, *args):
        self._append_chat("[system] refreshing users...")
        self._refresh_user_list(self.discovery.get_peers())

    def toggle_side_panel(self, *args):
        if self.side_panel.width > 0:
            self.side_panel.width = 0
            self.side_panel.opacity = 0
        else:
            self.side_panel.width = self.SIDE_WIDTH
            self.side_panel.opacity = 1

    def toggle_wifi(self, *args):
        if self.discovery._running:
            self.discovery.stop()
            self.btn_wifi.text = "WiFi: OFF"
        else:
            self.discovery.start()
            self.btn_wifi.text = "WiFi: ON"

    def toggle_bt(self, *args):
        self.btn_bt.text = "BT: soon"

    def select_target(self, peer):
        self.current_target = peer
        self.target_lbl.text = (
            f"Chatting with: {peer['nickname']} "
            f"({peer['ip']}:{peer.get('msg_port', '?')})"
        )
        self._append_chat(f"[system] selected {peer['nickname']}")

    def on_send(self, *args):
        text = self.msg_input.text.strip()
        if not text:
            return
        if not self.current_target:
            self._append_chat("[system] select a user first")
            return
        ok = self.messaging.send(
            self.current_target["ip"],
            self.current_target.get("msg_port", 50001),
            text
        )
        prefix = "Me" if ok else "Me (failed)"
        self._append_chat(f"{prefix}: {text}")
        self.msg_input.text = ""

    def _append_chat(self, line):
        self.chat_display.text += line + "\n"