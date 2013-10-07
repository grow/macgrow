"""Builds packaged application.

Usage:
  # For distribution.
  python setup.py py2app

  # For development (aliases).
  python setup.py py2app -A
"""

from distutils import core
import py2app


OPTIONS = {
  'iconfile': 'Icon.icns',
  'includes': [
    'BaseHTTPServer',
    'Queue',
    'cgi',
    'htmlentitydefs',
    'io',
    'json',
    'md5',
    'multiprocessing',
    'sha',
    'shutil',
    'urllib',
    'urllib2',
    'wsgiref',
    'wsgiref.handlers',
    'xml',
    'xml.etree.ElementTree',
  ]
}

# TODO(jeremydw): Executable data files should be moved to "app".

core.setup(
  app=[
    'MacGrow.py'
  ],
  data_files=[
    'MacGrow.nib',
    'MainMenu.nib',
    'VERSION',
    'cocoasudo',
    'pygrow',
    'symlinks.py',
  ],
  url='http://grow.io',
  options={'py2app': OPTIONS},
)
