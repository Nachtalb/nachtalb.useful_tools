import logging
import time

from Products.Five.browser import BrowserView
from zope.interface import implements

from nachtalb.useful_tools.interfaces import IUsefulToolsView


class UsefulToolsView(BrowserView):
    implements(IUsefulToolsView)

    def __init__(self, context, request):
        super(UsefulToolsView, self).__init__(context, request)
        self.logger = logging.getLogger('nachtalb.useful_tools - %s' % self.__class__.__name__)

    def get_logger(self):
        """Helper to prepend a time stamp to the output """
        write = self.request.RESPONSE.write

        def log(msg, prepend_newline=True, timestamp=True, warning=False):
            if warning:
                self.logger.warning(msg)
            else:
                self.logger.info(msg)

            if warning:
                msg = 'Warning - ' + msg
            if timestamp:
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
