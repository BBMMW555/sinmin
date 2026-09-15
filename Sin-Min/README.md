# Sin-Min

تطبيق محادثة محلية (LAN) يعمل على ويندوز وأندرويد بدون سيرفر مركزي.

## المبدأ
- كل جهاز يُعلن عن نفسه على شبكة الواي فاي عبر UDP Broadcast.
- عند اختيار مستخدم، تُرسل الرسائل مباشرة عبر TCP.
- لا يحتاج إنترنت، فقط نفس شبكة الواي فاي.

## التشغيل من الكود (ويندوز/لينكس)
```bash
pip install -r requirements.txt
python main.py

<!-- BuildHelper Metadata -->
App Name: Sin-Min
Framework: PyQt5
Entry File: C:/Users/bassam/Desktop/Sin-Min\main.py
Detected Imports: PyQt5, kivy, config
BuildHelper Version: BuildHelper Pro v2.3
Generated On: 2026-09-15 01:36:53
<!-- End BuildHelper Metadata -->