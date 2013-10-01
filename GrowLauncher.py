from Cocoa import *
from AppKit import NSBeep
from GrowLauncherModel import GrowLauncherModel

"""
import sys
sys.path.insert(0, '/Users/jeremydw/git/pygrow/')
import grow
from paste import httpserver

from grow.server import handlers
from grow.server import main as main_lib
handlers.set_single_pod_root('/Users/jeremydw/git/grow-templates')
"""


# class defined in PythonBrowser.nib
class GrowLauncherWindowController(NSWindowController):
    tableView = objc.IBOutlet()

    def __init__(self):
        self = self.initWithWindowNibName_('GrowLauncher')
        self.window().setTitle_('Grow Launcher')

        self.model = GrowLauncherModel()
        self.tableView.setDataSource_(self.model)
        self.tableView.setDelegate_(self.model)
        self.tableView.reloadData()
#        self.outlineView.setTarget_(self)
#        self.outlineView.setDoubleAction_("doubleClick:")
          #        self.window().makeFirstResponder_(self.tableView)
      
        # Show the window and bring it to the top.
        self.showWindow_(self)
        NSApp.activateIgnoringOtherApps_(True)
      
        # Prevent garbage collection before window is closed.
        # It will be released in self.windowWillClose_().
        self.retain()

    def __new__(cls):
      return cls.alloc().init()
  
    def windowWillClose_(self, notification):
        self.autorelease()

    @objc.IBAction
    def start_(self, sender):
        NSBeep()
        httpserver.serve(main_lib.services_app)
        print 'started'

    @objc.IBAction
    def stop_(self, sender):
        NSBeep()


class GrowLauncherAppDelegate(NSObject):

    def applicationDidFinishLaunching_(self, notification):
        GrowLauncherWindowController()


if __name__ == '__main__':
    from PyObjCTools import AppHelper
    AppHelper.runEventLoop()