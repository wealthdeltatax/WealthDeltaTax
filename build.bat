@echo off
echo Building WDT site...
python build_anchors.py
python preprocess.py
echo Rendering...
quarto render _build
echo Done. Open _build/_site/index.html to preview.
pause