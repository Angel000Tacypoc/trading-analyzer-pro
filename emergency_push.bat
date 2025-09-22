@echo off
echo 🚀 Emergency Push Script - Trading Analyzer Pro
echo ===============================================

echo 🔧 Killing any stuck Git processes...
taskkill /f /im git.exe 2>nul
taskkill /f /im notepad.exe 2>nul

echo 📂 Navigating to project directory...
cd /d "c:\Users\admin\Desktop\Programación\bingx\TradingAnalyzerWeb"

echo 🧹 Cleaning Git state...
git reset --hard HEAD 2>nul
git clean -fd 2>nul

echo 📋 Checking status...
git status

echo 📤 Adding all changes...
git add .

echo 📝 Committing changes...
git commit -m "🔧 HOTFIX: Modular architecture with unique element keys - fixes StreamlitDuplicateElementId"

echo 🚀 Force pushing to main...
git push --force-with-lease origin main

echo ✅ Done! Check Streamlit app for updates.
pause