from plone import api
from zope.interface import implements

from nachtalb.useful_tools.browser.useful_tools import UsefulToolsView
from nachtalb.useful_tools.interfaces import IMiscAnonToolsView


class MiscAnonToolsView(UsefulToolsView):
    implements(IMiscAnonToolsView)

    def pdb(self):
        """Start pdb at current context

        https://github.com/4teamwork/opengever.maintenance/blob/6d33009b189472fd912e5310eee18de089957f0c/opengever/maintenance/browser/configure.zcml#L86-L91
        """
        portal = api.portal.get()
        user = api.user.get_current()
        catalog = api.portal.get_tool('portal_catalog')

        self.context = self.get_non_ut_context()
        ppath = self.context.getPhysicalPath()
        path = '/'.join(ppath)
        brain = next(iter(catalog(path={'query': path, 'depth': 0})), None)

        __import__('pdb').set_trace()
        pass
        return "Done"
