# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [
    ('ETTP.db', '.'),
    ('JS00001.mat', '.'),
    ('fonts/*', 'fonts'),
    ('images/*', 'images')
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=['sklearn.metrics._pairwise_distances_reduction._datasets_pair', 'sklearn.metrics._pairwise_distances_reduction._middle_term_computer'],
    hookspath=[],
    hooksconfig={
        "matplotlib": {
            "backends": "svg"
        }
    },
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
    name='ETTP',
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
)

app = BUNDLE(
    exe,
    name='ETTP.app',
    icon='./images/icon.jpg',
    bundle_identifier='com.umn.ece.ettp'
)

