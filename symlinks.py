#/usr/bin/python

import logging
import os

_resource_path = os.environ['RESOURCEPATH']
GROW_COMMAND = os.path.join(_resource_path, 'pygrow', 'bin', 'grow')
GROW_SYMLINK = '/usr/local/bin/grow'
MACGROW_COMMAND = '/usr/local/bin/macgrow'
MACGROW_SYMLINK = os.path.join(_resource_path, 'macgrow_cli.sh')


def _install_symlink(source, dest):
  if os.path.exists(source):
    os.remove(source)
  os.symlink(dest, source)
  logging.info('Installed: {} -> {}'.format(source, dest))


def install_symlinks():
  _install_symlink(GROW_SYMLINK, GROW_COMMAND)
#  _install_symlink(MACGROW_SYMLINK, MACGROW_COMMAND)


def is_installed():
  return os.path.realpath(GROW_SYMLINK) == GROW_COMMAND


if __name__ == '__main__':
  install_symlinks()
