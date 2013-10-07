#/usr/bin/python

import logging
import os

_resource_path = os.environ['RESOURCEPATH']
GROW_COMMAND = os.path.join(_resource_path, 'pygrow', 'grow', 'cli.py')
GROW_SYMLINK = '/usr/local/bin/grow'


def install_symlinks():
  if os.path.exists(GROW_SYMLINK):
    os.remove(GROW_SYMLINK)
  os.symlink(GROW_COMMAND, GROW_SYMLINK)
  logging.info('Installed: {} -> {}'.format(GROW_COMMAND, GROW_SYMLINK))


if __name__ == '__main__':
  install_symlinks()
