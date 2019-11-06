from plone import api

try:
    from ftw.redirector.browser.fourohfour import CustomFourOhFourView as FourOhFourView
except ImportError:
    from plone.app.redirector.browser import FourOhFourView


class CustomFourOhFourView(FourOhFourView):
    REDIRECTS = {
        # 'alias': (is context specific, ('redirect', ' url')),
        'mm':  (True,  ('manage_main',)),
        'mmm': (False, ('manage_main',)),
        'mu':  (False, ('@@manage-upgrades',)),
        'oc':  (False, ('@@overview-controlpanel',)),
        'lg':  (False, ('@@lawgiver-list-specs',)),
        'uu':  (False, ('@@usergroup-userprefs',)),
        'tr':  (False, ('@@theming-resources',)),
        'pc':  (False, ('@@publisher-config',)),
        'trr': (False, ('test_rendering',)),
        'pr':  (False, ('portal_registry',)),
        'pt':  (False, ('portal_types', 'manage_main')),
        'ps':  (False, ('portal_setup', 'manage_main')),
        'pdb': (True,  ('useful-tools', 'misc-anon', 'pdb')),
        'ut':  (True,  ('useful-tools',)),
    }

    def attempt_redirect(self):
        path = self.request.physicalPathFromURL(self._url())
        context_specific, target = self.REDIRECTS.get(path[-1], [None, None])

        if not target:
            return super(CustomFourOhFourView, self).attempt_redirect()

        if context_specific:
            url = self.request.physicalPathToURL(path[:-1] + list(target))
        else:
            url = self.request.physicalPathToURL(api.portal.get().getPhysicalPath() + target)

        self.request.response.redirect(url, status=302, lock=1)
        return True
