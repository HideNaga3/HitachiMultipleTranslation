@echo off
echo "PUSH?"
pause
git add .
git commit -m "auto push"
git push origin main
pause
