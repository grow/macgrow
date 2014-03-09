# -*- mode: python -*-
a = Analysis(['pygrow/bin/grow'],
             pathex=['pygrow/', '/Users/jeremydw/git/macgrow', '/Library/Python/2.7/site-packages/'],
             hiddenimports=['markdown', 'markdown.extensions'],
             hookspath=None,
             runtime_hooks=None)
a.datas += [
    ('VERSION', '/Users/jeremydw/git/macgrow/pygrow/grow/VERSION', 'DATA'),
    ('server/templates/error.html', '/Users/jeremydw/git/macgrow/pygrow/grow/server/templates/error.html', 'DATA'),
]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='grow',
          debug=False,
          strip=None,
          upx=True,
          console=True,
          icon='macgrow/icon.icns')
