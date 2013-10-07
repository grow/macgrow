python setup.py py2app
cd dist
chmod +x MacGrow.app/Contents/Resources/cocoasudo
chmod +x MacGrow.app/Contents/Resources/pygrow/grow/cli.py
zip -r MacGrow.zip MacGrow.app
cd ..
