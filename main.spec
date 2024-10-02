a = Analysis(
    ["main.py"],
    binaries=None,
    datas=None,
    excludes=[],
    hiddenimports=[],
    hooksconfig={},
    hookspath=None,
    noarchive=False,
    optimize=0,
    pathex=[],
    runtime_hooks=None,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    argv_emulation=False,
    bootloader_ignore_signals=False,
    codesign_identity=None,
    console=False,
    debug=False,
    disable_windowed_traceback=False,
    entitlements_file=None,
    exclude_binaries=True,
    name="main",
    strip=False,
    target_arch=None,
    upx=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name="main",
    strip=False,
    upx_exclude=[],
    upx=True,
)
app = BUNDLE(coll, bundle_identifier=None, icon=None, name="main.app")
