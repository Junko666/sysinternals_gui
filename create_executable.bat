@echo off

:: Überprüfen, ob Python installiert ist
where python3 >nul 2>nul
if %errorlevel% neq 0 (
    echo Python ist nicht installiert. Installation wird gestartet...
    winget install Python.Python.3
) else (
    echo Python ist bereits installiert.
)

:: Überprüfen, ob pip installiert ist
python3 -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo pip ist nicht installiert. Installation wird gestartet...
    python3 -m ensurepip
) else (
    echo pip ist bereits installiert.
)

:: Überprüfen, ob pyinstaller installiert ist
python3 -m pyinstaller --version >nul 2>nul
if %errorlevel% neq 0 (
    echo pyinstaller ist nicht installiert. Installation wird gestartet...
    pip install pyinstaller
) else (
    echo pyinstaller ist bereits installiert.
)

:: Erstellen der ausführbaren Datei
pyinstaller --onefile --noconsole --icon=sysinternalssuitepy.ico sysinternals.py

pause
