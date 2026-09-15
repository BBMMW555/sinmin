# core/identity.py
# -*- coding: utf-8 -*-

import uuid
import json
import os
import sys


class Identity:
    """هوية المستخدم: ID فريد + اسم مستعار. تُحفظ محليًا."""

    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = self._default_storage_path()
        self.storage_path = storage_path
        self.user_id = None
        self.nickname = "User"
        self._load_or_create()

    @staticmethod
    def _default_storage_path():
        """مسار احتياطي إذا لم يُمرَّر storage_path."""
        # 1) Kivy app (يعمل على أندرويد)
        try:
            from kivy.app import App
            app = App.get_running_app()
            if app is not None and getattr(app, "user_data_dir", None):
                return os.path.join(app.user_data_dir, "identity.json")
        except Exception:
            pass

        # 2) داخل .exe على ويندوز
        if getattr(sys, "frozen", False):
            base = os.path.dirname(sys.executable)
            return os.path.join(base, "identity.json")

        # 3) تشغيل عادي بـ Python
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, "identity.json")

    def _load_or_create(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.user_id = data.get("user_id")
                    self.nickname = data.get("nickname", "User")
            except Exception:
                pass
        if not self.user_id:
            self.user_id = str(uuid.uuid4())[:8]
            self.save()

    def set_nickname(self, name):
        self.nickname = name or "User"
        self.save()

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        except Exception:
            pass
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump({"user_id": self.user_id, "nickname": self.nickname}, f)
        except Exception:
            pass