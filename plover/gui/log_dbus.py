
import logging

# Fix a possible crash...
# See: http://trac.wxwidgets.org/ticket/15898
import gtk
gtk.remove_log_handlers()

import pynotify

from plover import log, __name__ as __software_name__


pynotify.init(__software_name__.capitalize())


class DbusNotificationHandler(logging.Handler):
    """ Handler using DBus notifications to show messages. """

    def __init__(self):
        super(DbusNotificationHandler, self).__init__()
        self.setLevel(log.WARNING)
        self.setFormatter(log.NoExceptionTracebackFormatter('%(levelname)s: %(message)s'))

    def emit(self, record):
        level = record.levelno
        message = self.format(record)
        if level <= log.INFO:
            timeout = 10
            urgency = 0
        elif level <= log.WARNING:
            timeout = 15
            urgency = 1
        else:
            timeout = 0
            urgency = 2
        n = pynotify.Notification(__software_name__.capitalize(), message)
        n.set_timeout(timeout * 1000)
        n.set_urgency(urgency)
        n.show()

