from Products.Five.browser import BrowserView
from nachtalb.useful_tools.interfaces import IRedirects
from plone import api
from zope.interface import implements


class RedirectView(BrowserView):
    implements(IRedirects)

    def redirect_to(self, obj=None, view=None):
        if not obj:
            obj = api.portal.get()

        self.request.response.redirect(obj.absolute_url() + ('/%s' % view if view else ''))

    def mm(self):
        """Redirect to manage_main
        """
        self.redirect_to(view='manage_main')

    def mu(self):
        """Redirect to @@manage-upgrades
        """
        self.redirect_to(view='@@manage-upgrades')

    def oc(self):
        """Redirect to @@overview-controlpanel
        """
        self.redirect_to(view='@@overview-controlpanel')

    def pr(self):
        """Redirect to portal_registry
        """
        self.redirect_to(view='portal_registry')

    def lg(self):
        """Redirect to @@lawgiver-list-specs
        """
        self.redirect_to(view='@@lawgiver-list-specs')
