### Get RSS titles to database and show in MoinMoin

#### Preconfigure

- feeds.py, newdays.py, utils.py - put together into same directory
- FeedShow.py - put into macro directory. Ex., <i>moinmoin/wiki/data/plugin/macro/</i>
- fedsdb - put into directory accessable for <i>FeedShow.py</i> and writable for <i>feeds.py</i>

#### Configure

- DATABASE, WIKI, PARENTPAGE, TEMPLATEPAGE, EDITOR, UID and GID - must be currect in <i>feeds.py</i>
- DATABASE and PAGE_LINK - must be currect in <i>FeedShow.py</i>
- MOINMOIN_PATH, MOINMOIN_PATH_SUP and MOINMOIN_PATH_WIKI - must be currect in <i>newday.py</i>

<i>feeds.py</i> - run into the <b>cron</b> as frequently as necessary. Ex., 



#### MoinMoin use

#### Database
