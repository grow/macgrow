from Cocoa import *
from AppKit import *
from Foundation import *

import os
import urllib
import subprocess
import webbrowser
import sys
sys.path.insert(0, os.path.join(os.environ['RESOURCEPATH'], 'pygrow'))

from GrowLauncherModel import GrowLauncherModel
from grow.server import manager

# /usr/local/bin

VERSION = open(os.path.join(os.environ['RESOURCEPATH'], 'VERSION')).read().strip()


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

    check_for_updates(quiet=True)

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
    check_for_updates(quiet=False)


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
    GrowLauncherWindowController()


def alert(message="Default Message", info_text="", buttons=["OK"]):
  ap = Alert(message)
  ap.informativeText = info_text
  buttons.reverse()
  ap.buttons = buttons
  ap.displayAlert()
  return ap.buttonPressed


def check_for_updates(quiet=False):
  # Verify data.
  version_manifest = 'https://raw.github.com/grow/macgrow/master/LICENSE'
  try:
    version = urllib.urlopen(version_manifest).read()
  except:
    if quiet:
      return
    raise
  their_version = version.strip().replace('.', '')
  this_version = VERSION.replace('.', '')
  if their_version > this_version:
    message = 'A new version of Grow ({}) is ready to download.'.format(version.strip())
    resp = alert(message=message, buttons=['Visit site', 'Cancel'])
    if resp == 1001:
      webbrowser.open('http://about.grow.io/macgrow')
    return
  if not quiet:
    if this_version > their_version:
      info_text = 'And, yours is newer! ({})'.format(VERSION)
    else:
      info_text = ''
    alert('Awesome! You have the latest version of Grow ({}).'.format(version.strip()),
          info_text=info_text)


if __name__ == '__main__':
  from PyObjCTools import AppHelper
  AppHelper.runEventLoop()
