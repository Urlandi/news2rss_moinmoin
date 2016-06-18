# -*- coding: utf-8 -*-

from os import path as dirs
from datetime import datetime
import sqlite3 as db

import feedparser

from utils import tuple2date
from newday import newday

DATABASE = "feedsdb"

WIKI = r"http://www.moinmoin.examle/wiki/"
PARENTPAGE = u"Feeds"
TEMPLATEPAGE = u"TemlateFeeds"
EDITOR = u"Administrator"
UID = "apache"
GID = "apache"

def getfeeds(NameDb=DATABASE):

    FeedsCon = None
    Date = None

    try:
        FeedsCon = db.connect(NameDb)
        FeedsCon.row_factory = db.Row
        FeedsCur = FeedsCon.cursor()
        FeedsCur.execute("SELECT * FROM Feeds WHERE Feeds.Actual = 1")
        Feeds = FeedsCur.fetchall()

        for f in Feeds:
            if f["Modified"]:
                NewsList = feedparser.parse(f["Source"], modified=f["Modified"])
            elif f["Etag"]:
                NewsList = feedparser.parse(f["Source"], modified=f["Etag"])
            else:
                NewsList = feedparser.parse(f["Source"])

            FeedsCur.execute("SELECT Link FROM News WHERE News.FeedsId = %d ORDER BY Published DESC LIMIT %d" %
                             (f["FeedsId"], len(NewsList.entries)))
            BaseListRaw = FeedsCur.fetchall()
            BaseList = [i for sublist in BaseListRaw for i in sublist]

            FNews = True

            for news in NewsList.get("entries"):
                Link = news.get("feedburner_origlink",news.get("link"))
                if Link not in BaseList:
                    DateNow=tuple2date(news.get("modified_parsed",news.get("published_parsed",
                        datetime.utcnow().utctimetuple())))
                    Title=news.get('title',"%s %s" % (f["Name"],Link))

                    try:
                        FeedsCon.execute("INSERT INTO News('FeedsId','Title','Link','Published') VALUES(%d,'%s','%s','%s');"\
                                % (f["FeedsId"], Title, Link, DateNow))
                        FeedsCon.commit()

                        if FNews:
                            Date = DateNow
                            FNews = False

                    except db.Error:
                        FeedsCon.rollback()
                        pass
            
            Modified = NewsList.get("modified")
            Etag = NewsList.get("etag")
            InsertQuery = ()
            if Modified:                
                InsertQuery = "Modified = '%s'" % Modified
            elif Etag:
                InsertQuery = "Etag = '%s'" % Etag
            if Modified or Etag:
                try:
                    FeedsCon.execute("UPDATE Feeds SET " + InsertQuery  + " WHERE FeedsId = %d" % f["FeedsId"])
                    FeedsCon.commit()
                except db.Error:
                    FeedsCon.rollback()
                    pass

    finally:
        if FeedsCon:
            FeedsCon.close()

    if Date:
        NewPage = Date[:10]
        newday(WIKI,PARENTPAGE,TEMPLATEPAGE,NewPage,EDITOR, UID, GID)

getfeeds(dirs.join(dirs.dirname(__file__),"",DATABASE))