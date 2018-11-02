from plone.api.portal import get_tool
from zope.interface import implements

from nachtalb.useful_tools.browser.useful_tools import UsefulToolsView
from nachtalb.useful_tools.interfaces import ISLToolsView


class SLToolsView(UsefulToolsView):
    implements(ISLToolsView)

    def get_sl_pages(self, as_object=False, filter_by_path=True):
        query = self.get_sl_pages_query(filter_by_path=filter_by_path)

        catalog = get_tool('portal_catalog')
        brains = catalog(**query)

        for brain in brains:
            if as_object:
                yield brain.getObject()
                continue
            yield brain

    def get_sl_pages_query(self, filter_by_path=True):
        query = {'provides': ['ftw.simplelayout.interfaces.ISimplelayout']}

        if filter_by_path:
            context = self.get_non_ut_context()
            path = '/'.join(context.getPhysicalPath())
            query.update({'path': {
                'query': path
            }})

        return query

    def show_pages(self):
        """Show all sl pages filtered by current path
        """
        logger = self.get_logger()
        brains = self.get_sl_pages()

        for brain in brains:
            logger('{id: <30} - {title: <30} - {path}'.format(
                id=brain.id,
                title=brain.Title or '',
                path=brain.getPath(),
            ))
