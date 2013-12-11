#!/bin/bash
rm -rf dist
python setup.py py2app
VERSION=`cat pygrow/VERSION`
cd dist
chmod +x Grow\ SDK.app/Contents/Resources/cocoasudo
chmod +x Grow\ SDK.app/Contents/Resources/pygrow/grow/cli.py
chmod +x Grow\ SDK.app/Contents/Resources/macgrow_cli.py
zip -r Grow-SDK-${VERSION}.zip Grow\ SDK.app
cd ..
echo "Built: dist/Grow-SDK-${VERSION}.zip"
