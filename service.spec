# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['service.py'],
    pathex=[],
    binaries=[],
    datas=[("./script.js", ".")],
    hiddenimports=[
                'uvicorn.logging',
                'uvicorn.loops',
                'uvicorn.loops.auto',
                'uvicorn.protocols',
                'uvicorn.protocols.http',
                'uvicorn.protocols.http.auto',
                'uvicorn.protocols.websockets',
                'uvicorn.protocols.websockets.auto',
                'uvicorn.lifespan',
                'uvicorn.lifespan.on',
                'uvicorn',
                'gunicorn.glogging',
                'service'
    ],
    hookspath=[],
    hooksconfig={},
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
    name='service',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
