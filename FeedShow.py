# -*- coding: utf-8 -*-

Dependencies = ['time']

DATABASE = "feedsdb"
MAX_LIMIT = 1000
NORM_LIMIT = 10

PAGE_LINK = u"Feeds"

def FeedShow (macro, Date, Tail, NameDb=DATABASE):

    from re import match as regexp
    from datetime import datetime
    import sqlite3 as db


    from news2.utils import date2rus, DATE_FMT

    FeedsCon = None
    FeedPage = []

    f = macro.formatter

    BaseQuery = "SELECT Title,Link,Published FROM News WHERE Publish=1"
    DateLimit = " AND Published GLOB '%s*'" % Date

    DataQuery = BaseQuery

    if Date:
        if regexp(r"^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$", Date):
            DataQuery = DataQuery + DateLimit
        else:
            if regexp(r"^@.*$", Date):
                Tail = NORM_LIMIT
            Date = None

    if 1 > Tail > MAX_LIMIT:
        Tail = MAX_LIMIT

    RowLimit = " ORDER BY Published DESC LIMIT %d" % Tail

    DataQuery = DataQuery + RowLimit

    try:
        FeedsCon = db.connect(NameDb)
        FeedsCon.row_factory = db.Row
        FeedsCur = FeedsCon.cursor()
        FeedsCur.execute(DataQuery)
        Feeds = FeedsCur.fetchall()

        FFeed = True
        for feed in Feeds:
            if not FFeed:
                FeedPage.append(f.rule())
            else:
                FFeed = False
                if Date == None:
                    Date = feed["Published"][:10]
                FeedPage.append(f.big(True)+f.strong(True)+f.pagelink(True,pagename=PAGE_LINK+'/'+Date) +
                                f.text(date2rus(datetime.strptime(Date,DATE_FMT).date())) +
                                f.url(False)+f.strong(False)+f.big(False))
                FeedPage.append(f.heading(True,4))
                FeedPage.append(f.heading(False,4))
                FeedPage.append(f.paragraph(True))

            FeedPage.append(f.url(True,href=feed["Link"])+f.icon("www")+f.text(feed["Title"])+f.url(False))

        if not FFeed:
            FeedPage.append(f.paragraph(False))

    except:
        FeedPage = ""

    finally:
        if FeedsCon:
            FeedsCon.close()

        return "".join(FeedPage)

def macro_FeedShow(macro, Date=None, Tail=NORM_LIMIT):
    from os import path as dirs

    NameDb = dirs.join(dirs.dirname(__file__),"",DATABASE)

    return FeedShow(macro, Date, Tail, NameDb)