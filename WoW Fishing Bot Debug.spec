# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['wow_fishing_bot_debug.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('logo.png', '.'),
        ('bobber_template.png', '.'),
        ('config.json', '.'),
        ('wow_fishing_bot_debug.py', '.')
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'cv2',
        'numpy',
        'PIL',
        'PIL.ImageGrab',
        'pyautogui'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='WoW Fishing Bot Debug',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.png'
) 