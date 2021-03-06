try:
    from ftw.simplelayout.configuration import synchronize_page_config_with_blocks
    synchronize_available = True
except ImportError:
    synchronize_available = False

import transaction
from zope.interface import implements

from nachtalb.useful_tools.browser.useful_tools import UsefulToolsView
from nachtalb.useful_tools.interfaces import ISLToolsView
from nachtalb.useful_tools.utils import ItemGenerator, bool_request_argument


class SLToolsView(UsefulToolsView):
    implements(ISLToolsView)

    def get_sl_items(self, pages=True, blocks=True, as_object=False, filter_by_path=True):
        return ItemGenerator(query=self.get_sl_items_query(pages=pages, blocks=blocks, filter_by_path=filter_by_path),
                             as_object=as_object)

    def get_sl_items_query(self, pages=True, blocks=True, filter_by_path=True):
        interfaces = {'query': [], 'operator': 'or'}
        if pages:
            interfaces['query'].append('ftw.simplelayout.interfaces.ISimplelayout')
        if blocks:
            interfaces['query'].append('ftw.simplelayout.interfaces.ISimplelayoutBlock')

        if not (pages and blocks):
            interfaces['operator'] = 'and'

        query = {'object_provides': interfaces}

        if filter_by_path:
            context = self.get_non_ut_context()
            path = '/'.join(context.getPhysicalPath())
            query.update({'path': {
                'query': path
            }})

        return query

    def show_objects(self):
        """Show all sl objects filtered by current path
        """
        logger = self.get_logger(with_timestamp=False)

        blocks = bool_request_argument(self.request, ['blocks', 'block'], default=True)
        pages = bool_request_argument(self.request, ['pages', 'page'], default=True)

        if not blocks and not pages:
            logger.info('Search for sl blocks and sl pages disabled.. hence nothing found... who would have thought that...')
            return

        brains = self.get_sl_items(pages=pages, blocks=blocks)

        for brain in brains:
            logger.info('{id: <30} - {title: <30} - {path}'.format(
                id=brain.id,
                title=brain.Title or '',
                path=brain.getPath(),
            ))
        else:
            logger.info('No blocks/pages found')

    def synchronize(self):
        """Run synchronize page configuration on all sl sub pages starting with the current path
        """
        logger = self.get_logger()
        if not synchronize_available:
            logger.warning('Synchronization is available the ftw.simplelayout version used.')
            return

        timer = self.start_timer()
        context = self.get_non_ut_context()

        total_numbers = {
            'removed': 0,
            'added': 0
        }
        logger.info('Synchronizing Page Configurations for sl pages beyond {}'.format(
            '/'.join(context.getPhysicalPath())))
        logger.info('-' * 80)

        objects = self.get_sl_items(blocks=False, as_object=True)
        for index, obj in enumerate(objects):
            result = synchronize_page_config_with_blocks(obj)
            logger.info('Synchronized {index}/{total_amount} {title}: {result}'.format(
                index=index + 1,
                total_amount=len(objects),
                title=obj.Title(),
                result=result))

            total_numbers['removed'] += len(result['removed'])
            total_numbers['added'] += len(result['added'])

        transaction.commit()
        time = timer.stop()
        logger.info('-' * 80)
        logger.info('processed {items} items in {time}s, removed config entries {total[removed]}, added config '
               'entries {total[added]}'.format(items=len(objects), time=time, total=total_numbers))
