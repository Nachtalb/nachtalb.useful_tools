import logging
import time

from Acquisition import aq_parent
from Products.Five.browser import BrowserView
from nachtalb.useful_tools.interfaces import IUsefulToolsView
from nachtalb.useful_tools.utils import bool_request_argument
from plone.app.customerize import registration
from zope.interface import implements
from zope.publisher.interfaces.browser import IBrowserRequest


class UsefulToolsView(BrowserView):
    implements(IUsefulToolsView)

    def __call__(self, *args, **kwargs):
        log = self.get_logger()
        if self.__class__.__base__ is not UsefulToolsView:
            views_tuples = self.__ac_permissions__
            for view_tuple in views_tuples:
                permission, views = view_tuple
                map(lambda view: log(view, timestamp=False), filter(None, views))
        else:
            views = registration.getViews(IBrowserRequest)
            for view in views:
                view_class = getattr(view.factory, '__base__', None)
                if UsefulToolsView in getattr(view_class, '__bases__', []):
                    log(view.name, timestamp=False)

    def __init__(self, context, request):
        super(UsefulToolsView, self).__init__(context, request)
        self.logger = logging.getLogger('nachtalb.useful_tools - %s' % self.__class__.__name__)

    def get_logger(self, mime_type=None, charset=None):
        """Helper to prepend a time stamp to the output """
        write = self.request.RESPONSE.write

        mime_type = mime_type or 'text/plain'
        charset = charset or 'utf-8'
        self.request.RESPONSE.addHeader('Content-Type', '{}; charset={}'.format(mime_type, charset))

        timestamp_override = bool_request_argument(self.request, 'timestamp', default=True)

        def log(msg, prepend_newline=True, timestamp=True, warning=False):
            if warning:
                self.logger.warning(msg)
            else:
                self.logger.info(msg)

            if warning:
                msg = 'Warning - ' + msg
            if timestamp_override and timestamp:
                msg = time.strftime('%Y/%m/%d-%H:%M:%S ') + msg
            if prepend_newline:
                msg += '\n'
            write(msg)

        return log

    def start_timer(self):
        start_time = time.clock()

        class Timer:
            def __init__(self, start_time=None):
                self.start_time = start_time

            def stop(self):
                return time.clock() - self.start_time

            elapsed = stop

        return Timer(start_time)

    def get_non_ut_context(self):
        """Get non useful tools context"""
        context = self.context
        while IUsefulToolsView.providedBy(context):
            context = aq_parent(context)

        return context
