# Add at the top
import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)  # Fix for Python 3.13

# Modify the Analysis block
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('user_data/*', 'user_data'),  # Include data directory
        ('assets/*', 'assets')
    ],
    hiddenimports=[
        'PyPDF2._utils',
        'PyPDF2._reader',
        'PyPDF2._writer',
        'pathlib'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pkg_resources'],  # Exclude deprecated package
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)