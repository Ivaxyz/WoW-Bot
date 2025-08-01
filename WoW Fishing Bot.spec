# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['wow_fishing_bot_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('logo.png', '.'),
        ('bobber_template.png', '.'),
        ('config.json', '.'),
        ('wow_fishing_bot.py', '.')
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog'
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
    name='WoW Fishing Bot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.png'
)
