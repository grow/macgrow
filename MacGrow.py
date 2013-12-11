from Cocoa import *
from AppKit import *
from Foundation import *

import os
_resource_path = os.environ['RESOURCEPATH']

import logging
import pipes
import threading
import subprocess
import webbrowser
import sys
sys.path.insert(0, os.path.join(_resource_path, 'pygrow'))

import symlinks
from GrowLauncherModel import GrowLauncherModel
from grow.server import manager
from grow.common import sdk_utils

# /usr/local/bin

GROW_COMMAND = os.path.join(_resource_path, 'pygrow', 'grow', 'cli.py')
GROW_SYMLINK = '/usr/local/bin/grow'


class GrowLogWindowController(NSWindowController):
  textView = objc.IBOutlet()

  def __init__(self):
    self = self.initWithWindowNibName_('MacGrow')


# class defined in PythonBrowser.nib
class GrowLauncherWindowController(NSWindowController):
  tableView = objc.IBOutlet()

  def __init__(self):
    self = self.initWithWindowNibName_('MacGrow')
    self.window().setTitle_('Grow')

    self.model = GrowLauncherModel()
    self.tableView.setDataSource_(self.model)
    self.tableView.setDelegate_(self.model)
    self.tableView.reloadData()
#    self.outlineView.setTarget_(self)
#    self.outlineView.setDoubleAction_("doubleClick:")
      #    self.window().makeFirstResponder_(self.tableView)

    # Show the window and bring it to the top.
    self.showWindow_(self)
    NSApp.activateIgnoringOtherApps_(True)

    if not symlinks.is_installed():
      _alert_and_make_symlinks()

    thread = threading.Thread(target=check_for_updates)
    thread.start()

    # Prevent garbage collection before window is closed.
    # It will be released in self.windowWillClose_().
    self.retain()

  def __new__(cls):
    return cls.alloc().init()

  def windowWillClose_(self, notification):
    manager.stop_all()
    self.autorelease()

  def _getSelectedServer(self):
    selectedRow = self.tableView.selectedRow()
    return self.model.servers[selectedRow]

  @objc.IBAction
  def start_(self, sender):
    server = self._getSelectedServer()
    server.start()
    self.tableView.reloadData()

  @objc.IBAction
  def stop_(self, sender):
    server = self._getSelectedServer()
    server.stop()
    self.tableView.reloadData()

  @objc.IBAction
  def open_(self, sender):
    server = self._getSelectedServer()
    if not server.is_started:
      server.start()
      self.tableView.reloadData()
    webbrowser.open('http://localhost:{}'.format(server.port))

  @objc.IBAction
  def goHelp_(self, sender):
    webbrowser.open('http://docs.grow.io/macgrow')

  @objc.IBAction
  def goEdit_(self, sender):
    server = self._getSelectedServer()
    if not server.is_started:
      server.start()
      self.tableView.reloadData()
    webbrowser.open('http://localhost:{}/_grow'.format(server.port))

  @objc.IBAction
  def goReveal_(self, sender):
    server = self._getSelectedServer()
    path = server.root
    subprocess.check_call(['open', '--', path])

  @objc.IBAction
  def checkForUpdatesAction_(self, sender):
    check_for_updates()

  @objc.IBAction
  def makeSymlinksAction_(self, sender):
    if symlinks.is_installed():
      info_text = 'The Grow commands have already been installed to /usr/local/bin/grow.'
      alert(message='Grow commands already installed.', info_text=info_text)
      return
    _alert_and_make_symlinks()


def _alert_and_make_symlinks():
  message = 'Install Grow commands?'
  info_text = ('The "grow" command line utility can be installed on your Mac by creating a '
               'symlink in /usr/local/bin/grow.\n\nAn authorization will be required.')
  resp = alert(message=message, info_text=info_text, buttons=['OK', 'Cancel'])
  if resp != 1000:
    return
  path = pipes.quote(os.path.join(_resource_path, 'cocoasudo'))
  symlink_command = pipes.quote(os.path.join(_resource_path, 'symlinks.py'))
  command = '{} --prompt="Grow wants to make changes." python {}'.format(path, symlink_command)
  subprocess.call(command, shell=True)
  info_text = 'Now you can open Terminal and run "grow" to use the SDK.'
  alert(message='Grow commands installed.', info_text=info_text)


class Alert(object):

  def __init__(self, messageText):
    super(Alert, self).__init__()
    self.messageText = messageText
    self.informativeText = ""
    self.buttons = []

  def displayAlert(self):
    alert = NSAlert.alloc().init()
    alert.setMessageText_(self.messageText)
    alert.setInformativeText_(self.informativeText)
    alert.setAlertStyle_(NSInformationalAlertStyle)
    for button in self.buttons:
      alert.addButtonWithTitle_(button)
    NSApp.activateIgnoringOtherApps_(True)
    self.buttonPressed = alert.runModal()


class GrowLauncherAppDelegate(NSObject):

  def applicationDidFinishLaunching_(self, notification):
    if check_for_updates():
      AppHelper.stopEventLoop()  # Exit if the user opened the web browser.
      return

    if symlinks.is_installed():
      alert('The "grow" command is already installed. Open Terminal and run "grow" to use the SDK.')
    else:
      _alert_and_make_symlinks()

    AppHelper.stopEventLoop()
#    GrowLauncherWindowController()


def alert(message='Default Message', info_text='', buttons=['OK']):
  ap = Alert(message)
  ap.informativeText = info_text
  ap.buttons = buttons
  ap.displayAlert()
  return ap.buttonPressed


def check_for_updates():
  their_version = sdk_utils.get_latest_version()
  this_version = sdk_utils.get_this_version()
  if their_version > this_version:
    message = 'A new version of the Grow SDK is ready to download.'
    info_text = 'Your version: {}, Latest version: {}'.format(this_version, their_version)
    resp = alert(message=message, buttons=['Visit site', 'Cancel'], info_text=info_text)
    if resp == 1000:
      webbrowser.open('http://growapp.org')
      return True
  else:
    info_text = 'Your version: {}, Latest version: {}'.format(this_version, their_version)
    alert('You have the latest version of the Grow SDK ({}).'.format(this_version), info_text=info_text)


if __name__ == '__main__':
  from PyObjCTools import AppHelper
  AppHelper.runEventLoop()
