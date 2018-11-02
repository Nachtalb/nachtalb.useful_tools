from ftw.simplelayout.configuration import synchronize_page_config_with_blocks
from plone.api.portal import get_tool
import transaction
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

    def synchornize(self):
        """Run synchronize page configuration on all sl sub pages starting with the current path
        """
        logger = self.get_logger()
        timer = self.start_timer()
        context = self.get_non_ut_context()

        total_numbers = {
            'removed': 0,
            'added': 0
        }
        logger('Synchronizing Page Configurations for sl pages beyond {}'.format(
            '/'.join(context.getPhysicalPath())))
        logger('-' * 80)

        brains = self.get_sl_pages()
        for index, brain in enumerate(brains):
            result = synchronize_page_config_with_blocks(brain.getObject())
            logger('Synchronized {index}/{total_amount} {title}: {result}'.format(
                index=index,
                total_amount=len(brains),
                title=brain.Title,
                result=result))

            total_numbers['removed'] += len(result['removed'])
            total_numbers['added'] += len(result['added'])

        transaction.commit()
        time = timer.stop()
        logger('-' * 80)
        logger('processed {items} items in {time}s, removed config entries {total[removed]}, added config '
               'entries {total[added]}'.format(items=len(brains), time=time, total=total_numbers))
