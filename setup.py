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

core.setup(
  app=[
    'MacGrow.py'
  ],
  data_files=[
    'MacGrow.nib',
    'MainMenu.nib',
    'VERSION',
    'pygrow',
  ],
  url='http://grow.io',
  options={'py2app': OPTIONS},
)
