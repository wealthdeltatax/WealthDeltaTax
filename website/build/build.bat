@echo off
cd /d "%~dp0..\.."

echo Building WDT site...

python website\build\scrape_contents.py --write
if errorlevel 1 (
    echo FAILED: scrape_contents.py
    pause
    exit /b 1
)

python website\build\build_glossary.py --papers "papers\legacy" --contents "website\registry\contents.yml" --out "website\site\pages\glossary.md"
if errorlevel 1 (
    echo FAILED: build_glossary.py
    pause
    exit /b 1
)

python website\build\build_anchors.py
if errorlevel 1 (
    echo FAILED: build_anchors.py
    pause
    exit /b 1
)

python website\build\preprocess.py
if errorlevel 1 (
    echo FAILED: preprocess.py
    pause
    exit /b 1
)
echo Build complete.
pause