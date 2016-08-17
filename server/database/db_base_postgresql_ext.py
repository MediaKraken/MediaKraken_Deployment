# from psycopg2 documentation

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import datetime
import psycopg2
import psycopg2.extensions


class LoggingCursor(psycopg2.extensions.cursor):
    def execute(self, sql, args=None):
        logger = logging.getLogger('sql_debug')
        logger.info(self.mogrify(sql, args))
        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
        except Exception, exc:
            logger.error("%s: %s" % (exc.__class__.__name__, exc))
            raise


class InfDateAdapter:
    def __init__(self, wrapped):
        self.wrapped = wrapped
    def getquoted(self):
        if self.wrapped == datetime.date.max:
            return b"'infinity'::date"
        elif self.wrapped == datetime.date.min:
            return b"'-infinity'::date"
        else:
            return psycopg2.extensions.DateFromPy(self.wrapped).getquoted()


# cur = conn.cursor(cursor_factory=LoggingCursor)
# psycopg2.extensions.register_adapter(datetime.date, InfDateAdapter)