@echo off
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --icon "sysinternalssuitepy.ico"  "sysinternals.py"
