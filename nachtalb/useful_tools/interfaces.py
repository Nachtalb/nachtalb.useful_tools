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


class IMiscToolsView(Interface):
    """Miscellaneous tools"""

    def page_counter(self):
        """Count objects of a site with multi language support"""

    def page_counter_json(self):
        """Return page counter info as json
        """


class IMiscAnonToolsView(Interface):
    """Miscellaneous tools that can be accessed by anonymous user"""

    def pdb(self):
        """Start pdb at current context

        https://github.com/4teamwork/opengever.maintenance/blob/6d33009b189472fd912e5310eee18de089957f0c/opengever/maintenance/browser/configure.zcml#L86-L91
        """
