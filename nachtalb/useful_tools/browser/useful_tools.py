import logging
import time

from Acquisition import aq_parent
from Products.Five.browser import BrowserView
from nachtalb.useful_tools.interfaces import IUsefulToolsView
from plone.app.customerize import registration
from zope.interface import implements
from zope.publisher.interfaces.browser import IBrowserRequest


class UsefulToolsView(BrowserView):
    implements(IUsefulToolsView)

    def __call__(self, *args, **kwargs):
        logger = self.get_logger(with_timestamp=False)
        if self.__class__.__base__ is not UsefulToolsView:
            views_tuples = self.__ac_permissions__
            for view_tuple in views_tuples:
                permission, views = view_tuple
                map(lambda view: logger.info(view), filter(None, views))
        else:
            views = registration.getViews(IBrowserRequest)
            for view in views:
                view_class = getattr(view.factory, '__base__', None)
                if UsefulToolsView in getattr(view_class, '__bases__', []):
                    logger.info(view.name)

    def get_logger(self, mime_type=None, charset=None, with_timestamp=True, level=None):
        """Helper to prepend a time stamp to the output """
        mime_type = mime_type or 'text/plain'
        charset = charset or 'utf-8'
        level = level or logging.DEBUG

        self.request.RESPONSE.addHeader('Content-Type', '{}; charset={}'.format(mime_type, charset))

        logging_format = '%(levelname)s - %(message)s'
        if with_timestamp:
            logging_format = '%(asctime)s - ' + logging_format

        formatter = logging.Formatter(logging_format)

        response_handler = logging.StreamHandler(self.request.RESPONSE)
        response_handler.setFormatter(formatter)

        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(level)
        logger.handlers = []  # Remove handlers from previews call of this view
        logger.addHandler(response_handler)

        return logger

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
