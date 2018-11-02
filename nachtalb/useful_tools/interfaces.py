from zope.interface import Interface


class INachtalbUsefulToolsLayer(Interface):
    """Request layer for nachtalb.useful_tools"""


class IUsefulToolsView(Interface):
    """Useful tools base"""


class ISLToolsView(Interface):
    """ftw.simepllayout Toolbox"""

    def show_objects(self):
        """Find all Simplalayout objects beyond the context"""

    def synchronize(self):
        """Find all Simplalayout pages beyond the context and synchronize their
        page configuration"""


class ITrashToolsView(Interface):
    """ftw.trash Toolbox"""

    def clear_trash(self):
        """Clear the trash"""

    def cleanup(self):
        """Clear the trash and run solr cleanup"""
