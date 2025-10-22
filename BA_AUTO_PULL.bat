@echo off
echo "PULL?"
pause
git fetch origin
git pull --rebase origin main
pause

