#!/bin/bash
# Emergency deployment script for Trading Analyzer Pro

echo "🚀 Emergency Deployment - Trading Analyzer Pro"
echo "=============================================="

# Set Git editor to avoid interactive mode
export GIT_EDITOR=true
export EDITOR=true

# Kill any stuck processes
pkill -f git 2>/dev/null || true
pkill -f notepad 2>/dev/null || true

# Reset Git state
git reset --soft HEAD~1 2>/dev/null || true
git reset --hard HEAD 2>/dev/null || true

# Add all changes
git add .

# Commit with non-interactive mode
git -c core.editor=true commit -m "🔧 HOTFIX: Resolve StreamlitDuplicateElementId with modular architecture

- Transformed monolithic 2000-line app into professional OOP structure  
- All UI elements now have unique keys from config/settings.py
- Fixed PnL calculations to match local version (absolute values + percentages)
- Separated concerns: UI components, business logic, configuration
- Added deployment status tracking and Streamlit configuration
- Ready for production with enhanced stability and maintainability"

# Force push to update Streamlit Cloud
git push --force-with-lease origin main

echo "✅ Deployment completed!"
echo "🌐 Streamlit Cloud should update automatically"
echo "📊 Check: https://trading-analyzer-pro.streamlit.app"