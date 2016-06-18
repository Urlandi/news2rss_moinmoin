# -*- coding: utf-8 -*-

from datetime import datetime

DATE_FMT = r"%Y-%m-%d"
DATETIME_FMT = r"%Y-%m-%d %H:%M:%S.%f%z"

MONTHRUS_R = (None,u"Января",u"Февраля",u"Марта",u"Апреля",u"Мая",u"Июня", \
        u"Июля",u"Августа",u"Сентября",u"Октября",u"Ноября",u"Декабря",)

def tuple2date (DateParsed):
    DateDate = datetime(DateParsed.tm_year,
        DateParsed.tm_mon,
        DateParsed.tm_mday,
        DateParsed.tm_hour,
        DateParsed.tm_min,
        DateParsed.tm_sec).strftime(DATETIME_FMT)
    return DateDate

def date2rus (Date):
    return "%(day)s %(month)s %(year)s" % \
            {'day':Date.day, \
            'month':MONTHRUS_R[Date.month], \
            'year':Date.year}
