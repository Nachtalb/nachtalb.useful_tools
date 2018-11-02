from plone.api.portal import get_tool


class ItemGenerator(object):
    def __init__(self, query=None, brains=None, as_object=None):
        if not query and not brains:
            raise ValueError('Either query or brains must be given.')
        elif query and brains:
            raise ValueError('You can only give a query or brains, but not both')

        self.brains = brains

        if query:
            self.brains = get_tool('portal_catalog')(**query)

        self.as_object = as_object

    def __len__(self):
        return len(self.brains)

    def __iter__(self):
        for brain in self.brains:
            if self.as_object:
                yield brain.getObject()
                continue
            yield brain


def bool_request_argument(request, names, default=False):
    if isinstance(names, str):
        names = [names]

    result = default
    for name in names:
        arg = request.get(name, None)

        if arg in ['yes', 'enable', 'activate', 'on', '1']:
            result = True
        elif arg in ['no', 'disable', 'deactivate', 'off', '0']:
            result = False

        if arg is not None:
            break

    return result
