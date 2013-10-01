from Foundation import NSObject
from AppKit import NSBeep



class Pod(NSObject):

  def __init__(self, root, port=8000):
    self.root = root
    self.port = port

  def __new__(cls, *args, **kwargs):
    return cls.alloc().init()

  @property
  def revision_status(self):
    pass

  @property
  def server_status(self):
    return 'off'

  def start_server(self):

    pass

  def stop_server(self):
    pass

  def set_root(self, root):
    self.root = root

  def set_port(self, port):
    self.port = port


class GrowLauncherModel(NSObject):
  """A delegate and a data source for NSTableView."""

  def __init__(self):
    self.pods = []
    self.pods.append(Pod('/foo/bar', port=8081))
    self.pods.append(Pod('/foo/baz', port=8000))

  def __new__(cls, *args, **kwargs):
    return cls.alloc().init()

  # NSTableViewDataSource methods.

  def numberOfRowsInTableView_(self, view):
    return len(self.pods)

  def tableView_objectValueForTableColumn_row_(self, view, col, item):
    pod = self.pods[item]
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
