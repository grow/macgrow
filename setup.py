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
}

core.setup(
  app=[
    'GrowLauncher.py'
  ],
  data_files=[
    'MainMenu.nib',
    'GrowLauncher.nib',
  ],
  options={'py2app': OPTIONS},
)
