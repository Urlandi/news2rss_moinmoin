### Get RSS titles to database and show in MoinMoin

#### Preconfigure

- feeds.py, newdays.py, utils.py - put together into same directory
- FeedShow.py - put into macro directory. Ex., <i>/srv/moinmoin/wiki/data/plugin/macro/</i>
- feedsdb - put into directory accessable for <i>FeedShow.py</i> and writable for <i>feeds.py</i>

#### Configure

- DATABASE, WIKI, PARENTPAGE, TEMPLATEPAGE, EDITOR, UID and GID - must be currect in <i>feeds.py</i>
- DATABASE and PAGE_LINK - must be currect in <i>FeedShow.py</i>
- MOINMOIN_PATH, MOINMOIN_PATH_SUP and MOINMOIN_PATH_WIKI - must be currect in <i>newday.py</i>

<b>feeds.py</b> - run into the <b>cron</b> as frequently as necessary. Ex., add to <i>/etc/crontab</i>:

<i>01 * * * * root exec python /srv/moinmoin/wiki/data/plugin/news2/feeds.py > /dev/null 2> /dev/null</i>

After that <feeds.py> fills database <i>feedsdb</i> properly and <i>news.py</i> make MoinMoin page in PARENTPAGE/r"%Y-%m-%d"

#### MoinMoin use

Use <i>FeedShow([Date[,Tail[,Database]]])</i> where are:
 - <b>Date</b> is r"%Y-%m-%d"
 - <b>Tail</b> is count of last rows from <b>Database</b>. 10 - default, -1 for all
 - <b>Database</b>, optional database name

Example use in PARENTPAGE/r"%Y-%m-%d": <i>\<\<FeedShow("2016-01-01",-1)\>\></i> or 

in PARENTPAGE as is <i>\<\<FeedShow\>\></i>.

See for http://www.elsv-v.ru/wiki/Лента.

#### Database

See for <i>[feedsdb.png](feedsdb.png)</i> or <i>[feedsdb.dia](feedsdb.dia)</i> for detailed database structure.

Use lightsql editor for cahnge <i>feedsdb</i> file.

Table <b>Feeds</b> - collects all requested feeds and table <b>News</b> - collects all feeds what had been got from Internet. <b>News/Publish</b> - adjust what news has will been publish.
