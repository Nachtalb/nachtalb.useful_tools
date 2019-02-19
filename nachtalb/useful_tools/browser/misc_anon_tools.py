from pkg_resources import get_distribution
from zope.interface import implements

from nachtalb.useful_tools.browser.useful_tools import UsefulToolsView
from nachtalb.useful_tools.interfaces import IMiscAnonToolsView


class MiscAnonToolsView(UsefulToolsView):
    implements(IMiscAnonToolsView)

    def reload(self):
        """Reload code without login
        """
        if not get_distribution('plone.reload'):
            self.request.RESPONSE.status = 501
            return 'Not reloaded'

        action = self.request.get('action', None)
        if action:
            self.request.form.setdefault('action', action)

        context = self.get_non_ut_context()
        reload_ = context.unrestrictedTraverse('/reload')
        return reload_()

    def pdb(self):
        """Start pdb at current context

        https://github.com/4teamwork/opengever.maintenance/blob/6d33009b189472fd912e5310eee18de089957f0c/opengever/maintenance/browser/configure.zcml#L86-L91
        """
        import pdb; pdb.set_trace()
        pass
        return "Done"
