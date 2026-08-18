@echo off
cd /d "%~dp0.."

echo Building WDT site...

python pipeline\build_anchors.py
if errorlevel 1 (
    echo FAILED: build_anchors.py
    pause
    exit /b 1
)

python pipeline\preprocess.py
if errorlevel 1 (
    echo FAILED: preprocess.py
    pause
    exit /b 1
)

echo Build complete.
pause