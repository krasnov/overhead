#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '2011.0413'
print 'ver:', __version__

import sqlite3
import web, uuid
render = web.template.render('templates/')
#render.cache = True

urls = [
    '(.*)/cdx/', 'cdx',
    '(.*)/cdx', 'cdx',
    '(.*)', 'cdx1',
]

class cdx1(object):
    def GET(self, name):
        web.header('Content-type', 'text/html; charset=utf-8')
        con = sqlite3.connect('overhead.sqlite')
        cur = con.cursor()
        i = web.input()
        rez = u'Привет, Гость'
        if i:
            try:
                if i.name and i.passw:
                    n = i.name
                    p = i.passw
                    sql = u"select * from auth where user=? and passw=?"
                    cur.execute(sql, (n, p))
                    r = cur.fetchall()
                    if r:
                        rez = r[0][1]
                        uid = uuid.uuid4()
                        sql = u"UPDATE auth SET sesion=? WHERE user=?"
                        cur.execute(sql, (uid.hex, n))
                        con.commit()
                        raise web.redirect('/cdx?sid='+uid.hex)

                    else:
                        rez = u'Нет таких'
            except:
                rez = u'Привет, Гость'
        else:
            rez = u'Привет, Гость'
        return render.index(rez)

class cdx(object):
    def GET(self, name):
        i = web.input()
        sid = i.get('sid', '')
        con = sqlite3.connect('overhead.sqlite')
        cur = con.cursor()
        sql = u"select * from auth where sesion=?"
        cur.execute(sql, (sid,))
        r = cur.fetchall()
        if r:
            rez = r[0][1]
        else:
            pass
            #raise web.redirect('/')
        web.header('Content-type', 'text/html; charset=utf-8')
        out = render.main({'name': rez, 'uuid': sid})
        #out.uuid
        return out


app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()
