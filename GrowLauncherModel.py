from Foundation import NSObject
from AppKit import NSBeep
from grow.server import manager


class Pod(NSObject, manager.PodServer):

  def __new__(cls, *args, **kwargs):
    return cls.alloc().init()


class GrowLauncherModel(NSObject):
  """A delegate and a data source for NSTableView."""

  def __init__(self):
    self.servers = manager.PodServer.load()

  def __new__(cls, *args, **kwargs):
    return cls.alloc().init()

  # NSTableViewDataSource methods.

  def numberOfRowsInTableView_(self, view):
    return len(self.servers)

  def tableView_objectValueForTableColumn_row_(self, view, col, item):
    pod = self.servers[item]
    parts = {
      'root': pod.root,
      'port': pod.port,
      'revision_status': pod.revision_status,
      'server_status': pod.server_status,
    }
    return parts.get(col.identifier(), None)

  def tableView_shouldEditTableColumn_item_(self, view, col, item):
    return True

  # NSOutlineViewDataSource methods.

  def outlineView_numberOfChildrenOfItem_(self, view, item):
    if item is None:
      item = self.root
    return len(item)

  def outlineView_child_ofItem_(self, view, child, item):
    if item is None:
      item = self.root
    return item.getChild(child)

  def outlineView_isItemExpandable_(self, view, item):
    if item is None:
      item = self.root
    return item.isExpandable()

  def outlineView_objectValueForTableColumn_byItem_(self, view, col, item):
    if item is None:
      item = self.root
    return getattr(item, col.identifier())

  # Delegate methods.

  def outlineView_shouldEditTableColumn_item_(self, view, col, item):
    return item.isEditable()
