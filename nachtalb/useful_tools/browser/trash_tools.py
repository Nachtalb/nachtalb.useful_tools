from copy import copy
import re

from ftw.trash.interfaces import IRestorable
from nachtalb.useful_tools.browser.useful_tools import UsefulToolsView
from nachtalb.useful_tools.interfaces import ITrashToolsView
from nachtalb.useful_tools.utils import ItemGenerator
from pkg_resources import DistributionNotFound, get_distribution
from plone import api
from zope.interface import implements


class TrashToolsView(UsefulToolsView):
    implements(ITrashToolsView)

    def clear_trash(self):
        """Clean the trash
        """
        logger = self.get_logger()
        portal = api.portal.get()
        trash_can = portal.unrestrictedTraverse('trash')

        trashed_query = {'object_provides': IRestorable.__identifier__, 'trashed': True}
        trashed_amount_before = len(ItemGenerator(trashed_query))

        # Get CSRF Token
        confirm_page = trash_can.confirm_clean_trash()
        tag = re.findall('<input[^>]+_authenticator.*?>', confirm_page)
        attributes = re.findall('(\S+)=["\']?((?:.(?!["\']?\s+(?:\S+)=|[>"\']))+.)["\']?', tag[0] if tag else '')
        attributes_dict = {key: value for (key, value) in attributes}
        csrf_token = attributes_dict.get('value')

        if not csrf_token:
            return 'Could not extract csrf token from confirm page'

        request = copy(self.request)
        request.environ['REQUEST_METHOD'] = 'POST'
        request.method = 'POST'
        request.form['_authenticator'] = csrf_token
        request.form['delete'] = 'Delete'

        trash_can.clean_trash(request)
        self.request.response.setStatus(200)
        del self.request.response.headers['location']

        trashed_query = {'object_provides': IRestorable.__identifier__, 'trashed': True}
        trashed_amount_after = len(ItemGenerator(trashed_query))

        logger('Clearing complete cleaned. Deleted {deleted_total}/{trashed_before} objects.'.format(
            deleted_total=trashed_amount_before - trashed_amount_after,
            trashed_before=trashed_amount_before
        ))

    def cleanup(self):
        """Clear the trash and run solr cleanup
        """
        try:
            get_distribution('collective.solr')
        except DistributionNotFound:
            return 'This view is for cleaning the trash and then run solr cleanup, ' \
                   'but collective.solr is not installed.'

        self.clear_trash()

        portal = api.portal.get()
        maintenance = portal.unrestrictedTraverse('@@solr-maintenance')
        maintenance.cleanup()
