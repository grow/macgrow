"""Builds packaged application.

Usage:
  # For distribution.
  python setup.py py2app

  # For development (aliases).
  python setup.py py2app -A
"""

from distutils import core
import py2app

VERSION = open('VERSION').read().strip()

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
  name='Grow',
  description='A fast, portable, simple, but powerful web site builder and file-based content management system for teams.',
  url='http://grow.io',
  author='Jeremy Weinstein',
  author_email='jeremydw@grow.io',
  version=VERSION,
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
    'macgrow_cli.sh',
  ],
  options={'py2app': OPTIONS},
)
