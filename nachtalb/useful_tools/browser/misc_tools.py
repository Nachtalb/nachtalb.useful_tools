from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from zope.interface import implements

from nachtalb.useful_tools.browser.useful_tools import UsefulToolsView
from nachtalb.useful_tools.interfaces import IMiscToolsView
from nachtalb.useful_tools.utils import ItemGenerator
from nachtalb.useful_tools.utils import bool_request_argument
from nachtalb.useful_tools.utils import list_request_argument

import json

NEW_TYPES = [
    'ftw.simplelayout.ContentPage',
    'ftw.events.EventPage',
    'ftw.events.EventFolder',
    'ftw.news.News',
    'ftw.news.NewsFolder',
    'FormFolder',
]

OLD_TYPES = [
    'ContentPage',
    'EventPage',
    'FormFolder',
    'News',
    'NewsFolder',
]


class MiscToolsView(UsefulToolsView):
    implements(IMiscToolsView)

    page_counter_template = ViewPageTemplateFile('templates/page_counter.pt')

    def pdb(self):
        """Start pdb at current context

        https://github.com/4teamwork/opengever.maintenance/blob/6d33009b189472fd912e5310eee18de089957f0c/opengever/maintenance/browser/configure.zcml#L86-L91
        """
        import pdb; pdb.set_trace()
        pass
        return "Done"

    def page_counter_query(self):
        old_types = bool_request_argument(self.request, 'old')
        pathfilter = bool_request_argument(self.request, 'pathfilter')
        clear = bool_request_argument(self.request, 'clear')
        types = list_request_argument(self.request, ('types', 'type'))
        types = filter(lambda item: item.strip(), types)

        query = {}

        searched_types = []
        if not clear:
            searched_types += NEW_TYPES if not old_types else OLD_TYPES

        for type_ in types:
            if type_.startswith('-') and type_.lstrip('-') in searched_types:
                searched_types.remove(type_.lstrip('-'))
            elif not type_.startswith('-'):
                searched_types.append(type_.lstrip('+'))

        if searched_types:
            query['portal_type'] = searched_types

        context = api.portal.get()
        if pathfilter:
            context = self.get_non_ut_context()
        context_path = '/'.join(context.getPhysicalPath())
        query['path'] = {'query': context_path}

        return query

    def page_counter(self):
        """Count objects of a site with multi language support
        """
        return self.page_counter_template(**{'infos': self._page_counter()})

    def _page_counter(self):
        query = self.page_counter_query()
        objects = ItemGenerator(query=query, as_object=True)

        search_result = {}
        language_dict = {}
        for obj in objects:
            search_result.setdefault(obj.portal_type, [])
            search_result[obj.portal_type].append(obj)

            language = obj.Language() or 'no language'
            language_dict.setdefault(language, 0)
            language_dict[language] += 1

        result = {
            'path': query['path']['query'],
            'old_types': bool_request_argument(self.request, 'old'),
            'cleared': bool_request_argument(self.request, 'clear'),
            'searched_types': query.get('portal_type', []),
            'total': len(objects),
            'languages': language_dict,
            'search_result': search_result,
        }

        return result

    def page_counter_json(self):
        """Return page counter info as json
        """
        info = self._page_counter()

        # We can't json serialize Plone objects so we replace them with a dict
        # containing the id, title, language, path and url
        search_result = {}
        for type_, objs in info['search_result'].items():
            search_result.setdefault(type_, [])

            for obj in objs:
                search_result[type_].append({
                    'id': obj.id,
                    'title': obj.Title(),
                    'langugage': obj.Language(),
                    'path': '/'.join(obj.getPhysicalPath()),
                    'url': obj.absolute_url()
                })

        info['search_result'] = search_result

        self.request.RESPONSE.addHeader('Content-Type',
                                        'application/json; charset=utf-8')
        return json.dumps(info, sort_keys=True, indent=4)
