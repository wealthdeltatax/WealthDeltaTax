@echo off
cd /d "%~dp0"

echo Building WDT site...

python build_anchors.py
if errorlevel 1 exit /b 1

python preprocess.py
if errorlevel 1 exit /b 1

echo Build complete.
pause