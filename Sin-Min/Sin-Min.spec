# Sin-Min.spec
# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import sdl2, glew
from PyInstaller.utils.hooks import collect_data_files
import os

block_cipher = None

# جمع ملفات Kivy
kivy_datas = collect_data_files('kivy')

# جمع assets إن وجدت
assets_datas = []
if os.path.isdir('assets'):
    for root, _, files in os.walk('assets'):
        for f in files:
            src = os.path.join(root, f)
            assets_datas.append((src, root))


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=kivy_datas + assets_datas,
    hiddenimports=[
        'kivy',
        'kivy.core.window',
        'kivy.core.text',
        'kivy.core.image',
        'kivy.uix.boxlayout',
        'kivy.uix.button',
        'kivy.uix.label',
        'kivy.uix.textinput',
        'kivy.uix.scrollview',
        'core.identity',
        'core.discovery',
        'core.messaging',
        'ui.main_screen',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Sin-Min',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,     # ← اجعلها False بعد نجاح البناء الأول
        icon=r'C:/Users/bassam/Desktop/Sin-Min\assets\icon.ico',
          
)
