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

