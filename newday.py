# -*- coding: utf-8 -*-

from sys import path

MOINMOIN_PATH = "/srv/moinmoin"
MOINMOIN_PATH_SUP = "/srv/moinmoin/MoinMoin/support"
MOINMOIN_PATH_WIKI = "/srv/moinmoin/wiki"

path.append(MOINMOIN_PATH)
path.append(MOINMOIN_PATH_SUP)
path.append(MOINMOIN_PATH_WIKI)

def newday (Wiki, ParentPage, TemplatePage, NewPage, Editor, UidName, GidName):

    from os import seteuid,setegid
    from pwd import getpwnam
    from grp import getgrnam

    uid = getpwnam(UidName).pw_uid
    gid = getgrnam(GidName).gr_gid

    setegid(gid)
    seteuid(uid)

    from MoinMoin.PageEditor import PageEditor
    from MoinMoin.Page import Page
    from MoinMoin.user import getUserId, User
    from MoinMoin.web.contexts import ScriptContext

    PageName = "%s/%s" % (ParentPage,NewPage)

    RequestPage = ScriptContext(Wiki, PageName)
    UserId = getUserId(RequestPage, Editor)
    RequestPage.user = User(RequestPage, UserId)

    Editor = PageEditor(RequestPage, PageName)
    Dummy, Revision, Exists = Editor.get_rev()

    if not Exists:

        RequestTemplate = ScriptContext(Wiki, TemplatePage)
        Viewer = Page(RequestTemplate, TemplatePage)

        Text = Viewer.getPageText().replace("@PAGE@", NewPage)
        Header = Viewer.getPageHeader()

        Text=Header+Text

        return Editor.saveText(Text, Revision)