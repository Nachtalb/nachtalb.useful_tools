from plone import api

try:
    from ftw.redirector.browser.fourohfour import CustomFourOhFourView as FourOhFourView
except ImportError:
    from plone.app.redirector.browser import FourOhFourView


class CustomFourOhFourView(FourOhFourView):
    REDIRECTS = {
        # 'alias': (is context specific, 'redirect url'),
        'mm': (True, 'manage_main'),
        'mmm': (False, 'manage_main'),
        'mu': (False, '@@manage-upgrades'),
        'oc': (False, '@@overview-controlpanel'),
        'lg': (False, '@@lawgiver-list-specs'),
        'uu': (False, '@@usergroup-userprefs'),
        'tr': (False, '@@theming-resources'),
        'trr': (False, 'test_rendering'),
        'pr': (False, 'portal_registry'),
        'pt': (False, 'portal_types/manage_main'),
        'ps': (False, 'portal_setup/manage_main'),
        'pdb': (True, 'useful-tools/misc-anon/pdb'),
        'ut': (True, 'useful-tools'),
    }

    def find_redirect(self, path):
        path = path.split('/')[-1]
        return self.REDIRECTS.get(path, [None, None])

    def attempt_redirect(self):
        context_specific, target = self.find_redirect(self.get_path())
        if not target:
            return super(CustomFourOhFourView, self).attempt_redirect()

        if '://' not in target:
            if context_specific:
                context = self.context
            else:
                context = api.portal.get()
            target = '{}/{}'.format(context.absolute_url(), target)

        self.request.response.redirect(target, status=301, lock=1)
