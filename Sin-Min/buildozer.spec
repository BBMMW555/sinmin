[app]
title = Sin-Min
package.name = sinmin
package.domain = org.sinmin

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,ico

version = 0.1.0

# المكتبات — انتبه: لا مسافات
requirements = python3,kivy

orientation = portrait
fullscreen = 0

# صلاحيات كاملة لكل إصدارات أندرويد
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,CHANGE_WIFI_MULTICAST_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,NEARBY_WIFI_DEVICES

android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a

android.accept_sdk_license = True

android.presplash_color = #222222
android.presplash_alpha = 1

android.allow_backup = 1
author = Bassam
android.wakelock = 0

# أيقونة التطبيق (لأندرويد تحتاج PNG 512×512)
# icon.filename = %(source.dir)s/assets/icon.png

android.logcat_filters = *:S python:D