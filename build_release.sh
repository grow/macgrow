#!/bin/bash
rm -rf dist
python setup.py py2app
VERSION=`cat pygrow/grow/VERSION`
cd dist
chmod +x Grow\ SDK.app/Contents/Resources/cocoasudo
chmod +x Grow\ SDK.app/Contents/Resources/pygrow/bin/grow
zip -r Grow-SDK-${VERSION}.zip Grow\ SDK.app
cd ..
echo "Built: dist/Grow-SDK-${VERSION}.zip"
