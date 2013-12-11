"""Builds packaged application.

Usage:
  # For distribution.
  python setup.py py2app

  # For development (aliases).
  python setup.py py2app -A
"""

from distutils import core
import py2app

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pygrow'))
from grow.common import sdk_utils


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
    'pipes',
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
  name='Grow SDK',
  description='A fast, portable, simple, but powerful web site builder and file-based content management system for teams.',
  url='http://growapp.org',
  author='Jeremy Weinstein',
  author_email='jeremydw@grow.io',
  version=sdk_utils.get_this_version(),
  app=[
    'MacGrow.py'
  ],
  data_files=[
    'MacGrow.nib',
    'MainMenu.nib',
    'cocoasudo',
    'pygrow',
    'symlinks.py',
    'macgrow_cli.sh',
  ],
  options={'py2app': OPTIONS},
)
