# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py/Applications/Xcode.app/Contents/Developer/usr/bin/python3', '/Users/je/Documents/2020.m4_6/python_project/shotDataVisualization/main.py'],
             pathex=['/Users/je/Documents/2020.m4_6/python_project/shotDataVisualization'],
             binaries=[],
             datas=[],
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
          name='python3',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
