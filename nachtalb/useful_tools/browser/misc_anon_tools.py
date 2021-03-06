import json

from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.uuid.interfaces import IUUID
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

    def info(self):
        """Show the objects UUID
        """
        context = self.get_non_ut_context()
        try:
            uuid = IUUID(context)
        except TypeError:
            uuid = None
        info = {
            'id': context.id,
            'title': context.Title(),
            'uuid': uuid,
            'portal_type': context.portal_type,
        }
        return json.dumps(info, indent=4, sort_keys=True, ensure_ascii=False)

    def filestat(self):
        """Show statistics of file sizes
        """
        template = ViewPageTemplateFile('templates/filesize.pt')
        brains_by_size = []
        limit = int(self.request.get('limit', 100))
        catalog = api.portal.get_tool('portal_catalog')
        path = '/'.join(self.get_non_ut_context().getPhysicalPath())


        for brain in catalog({'path': {'query': path}}):
            size, entity = brain.getObjSize.split(' ')
            if entity == 'GB':
                size = float(size) * 1024 * 1024 * 1024
            elif entity == 'MB':
                size = float(size) * 1024 * 1024
            elif entity == 'KB':
                size = float(size) * 1024
            else:
                continue

            brains_by_size.append((size, brain.getObjSize, brain))

        brains_by_size.sort(key=lambda item: item[0], reverse=True)

        entries = []
        for _, size, brain in brains_by_size[:limit]:
            entries.append({
                'size': size,
                'type': brain.portal_type,
                'url': brain.getURL(),
                'title': safe_unicode(brain.Title or brain.getId),
            })

        total = len(brains_by_size)
        return template(self, **{
            'entries': entries,
            'total': total,
            'shown': min((limit, total)),
            'next': '?limit=' + str(limit + 100),
            'limit': limit,
        })
