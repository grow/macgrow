#!/bin/bash
rm -rf dist
python setup.py py2app -A
cd dist
chmod +x Grow\ SDK.app/Contents/Resources/cocoasudo
chmod +x Grow\ SDK.app/Contents/Resources/pygrow/bin/grow
echo "Built: dist/Grow SDK.app"
