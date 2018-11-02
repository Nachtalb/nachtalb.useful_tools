from zope.interface import Interface


class INachtalbUsefulToolsLayer(Interface):
    """Request layer for nachtalb.useful_tools"""


class IUsefulToolsView(Interface):
    """Useful tools base"""


class ISLToolsView(Interface):
    """ftw.simepllayout Toolbox"""

    def show_pages(self):
        """Find all Simplalayout pages beyond the context"""

    def synchronize(self):
        """Find all Simplalayout pages beyond the context and synchronize their
        page configuration"""
