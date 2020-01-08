# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(1000000)
block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\YEPT\\YEPT-2.0\\YEPT'],
             binaries=[],
             datas=[('data', 'data'), ('lib', 'lib')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='YEPT',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='data\\YEPT.ico')
