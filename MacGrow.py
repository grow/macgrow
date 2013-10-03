from Cocoa import *
from AppKit import NSBeep

import os
import webbrowser
import sys
sys.path.insert(0, os.path.join(os.environ['RESOURCEPATH'], 'pygrow'))

from GrowLauncherModel import GrowLauncherModel
from grow.server import manager


# class defined in PythonBrowser.nib
class GrowLauncherWindowController(NSWindowController):
  tableView = objc.IBOutlet()

  def __init__(self):
    self = self.initWithWindowNibName_('MacGrow')
    self.window().setTitle_('MacGrow')

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

    # Prevent garbage collection before window is closed.
    # It will be released in self.windowWillClose_().
    self.retain()

  def __new__(cls):
    return cls.alloc().init()

  def windowWillClose_(self, notification):
    manager.stop_all()
    self.autorelease()

  @objc.IBAction
  def start_(self, sender):
    selectedRow = self.tableView.selectedRow()
    server = self.model.servers[selectedRow]
    server.start()
    self.tableView.reloadData()

  @objc.IBAction
  def stop_(self, sender):
    selectedRow = self.tableView.selectedRow()
    server = self.model.servers[selectedRow]
    server.stop()
    self.tableView.reloadData()

  @objc.IBAction
  def open_(self, sender):
    selectedRow = self.tableView.selectedRow()
    server = self.model.servers[selectedRow]
    webbrowser.open('http://localhost:{}'.format(server.port))

  @objc.IBAction
  def helpSite_(self, sender):
    webbrowser.open('http://docs.grow.io/macgrow')


class GrowLauncherAppDelegate(NSObject):

  def applicationDidFinishLaunching_(self, notification):
    GrowLauncherWindowController()


if __name__ == '__main__':
  from PyObjCTools import AppHelper
  AppHelper.runEventLoop()
