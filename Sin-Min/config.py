# config.py
# -*- coding: utf-8 -*-
"""
إعدادات التطبيق العامة.
- تعمل على ويندوز/لينكس/أندرويد.
- حجم النافذة يُطبق فقط على أنظمة سطح المكتب.
"""

from kivy.utils import platform

APP_NAME = "Sin-Min"
APP_VERSION = "0.1.0"

# ---------- الشبكة ----------
DISCOVERY_PORT      = 50000
MESSAGING_PORT      = 50001
BROADCAST_IP        = "255.255.255.255"
BROADCAST_INTERVAL  = 2.0    # ثواني بين كل إعلان
USER_TIMEOUT        = 10.0   # ثواني قبل اعتبار المستخدم غير متصل

# ---------- الواجهة ----------
# لا نضع Window.size على الجوال (Kivy يتجاهلها أو تسبب مشاكل)
if platform in ("win", "linux", "macosx"):
    WINDOW_SIZE = (420, 720)
else:
    WINDOW_SIZE = None

# هل نستخدم وضع الجوال (لتغييرات الواجهة لاحقًا)
IS_MOBILE = platform in ("android", "ios")