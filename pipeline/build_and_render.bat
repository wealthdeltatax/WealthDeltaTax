@echo off
cd /d "%~dp0.."

:: Ensure Quarto is on PATH for cmd.exe
set PATH=%PATH%;C:\Users\kyleo\AppData\Local\Programs\Quarto\bin

echo Building WDT site...

python pipeline\scrape_contents.py --write
if errorlevel 1 (
    echo FAILED: scrape_contents.py
    pause
    exit /b 1
)

python pipeline\build_glossary.py --papers "source" --contents "registry\contents.yml" --out "site\pages\glossary.md"
if errorlevel 1 (
    echo FAILED: build_glossary.py
    pause
    exit /b 1
)

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

quarto render _build
if errorlevel 1 (
    echo FAILED: quarto render _build
    pause
    exit /b 1
)

echo Build complete.
pause