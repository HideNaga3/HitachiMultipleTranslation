@echo off
cd /d "%~dp0.."
call .venv\Scripts\activate.bat
python control\run_process.py
pause
