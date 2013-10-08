#!/bin/bash
rm -rf dist
python setup.py py2app
VERSION=`cat VERSION`
cd dist
chmod +x Grow.app/Contents/Resources/cocoasudo
chmod +x Grow.app/Contents/Resources/pygrow/grow/cli.py
zip -r Grow-${VERSION}.zip Grow.app
cd ..
echo "Built: dist/Grow-${VERSION}.zip"
