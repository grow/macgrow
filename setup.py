"""Builds packaged application.

Usage:
  # For distribution.
  python setup.py py2app

  # For development (aliases).
  python setup.py py2app -A
"""

from distutils import core
import py2app
import setuptools
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pygrow'))
from grow.common import sdk_utils


OPTIONS = {
  'iconfile': 'icon.icns',
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
  ],
  'packages': setuptools.find_packages() + ['jinja2'],
}

# TODO(jeremydw): Executable data files should be moved to "app".
core.setup(
  name='Grow SDK',
    description=(
          'Develop everywhere and deploy anywhere: a declarative '
          'static site generator/CMS for building high-quality web sites.'
    ),
  url='http://growsdk.org',
  author='Grow SDK Authors',
  author_email='hello@grow.io',
  version=sdk_utils.get_this_version(),
  app=[
    'MacGrow.py'
  ],
  data_files=[
    'MacGrow.nib',
    'MainMenu.nib',
    'cocoasudo',
    'icon.png',
    'macgrow_cli.sh',
    'pygrow',
    'symlinks.py',
  ],
  options={'py2app': OPTIONS},
)
