#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '2011.0413'
print 'ver:', __version__

import sqlite3
import web, uuid
render = web.template.render('templates/')
#render.cache = True

urls = [
    '(.*)/exit', 'exit',
    '(.*)/users', 'users',
    '(.*)/main/', 'main',
    '(.*)/main', 'main',
    '(.*)/main', 'main',
    '(.*)', 'index',

]

class index(object):
    def GET(self, name):
        web.header('Content-type', 'text/html; charset=utf-8')
        con = sqlite3.connect('overhead.sqlite')
        cur = con.cursor()
        sid = web.cookies().get('sid')
        if sid:
            sql = u"select * from auth where sesion=?"
            cur.execute(sql, (sid,))
            r = cur.fetchall()
            if r:
                raise web.redirect('/main')

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
                        right = r[0][3]
                        print 'right:',right
                        uid = uuid.uuid4()
                        sql = u"UPDATE auth SET sesion=? WHERE user=?"
                        cur.execute(sql, (uid.hex, n))
                        con.commit()
                        web.setcookie('sid', uid.hex, 3600)
                        #raise web.redirect('/cdx?sid='+uid.hex)
                        if right==4:
                            raise web.redirect('/main')
                        else:
                            raise web.redirect('/users')

                    else:
                        rez = u'Нет таких'
            except:
                rez = u'Привет, Гость'
        else:
            rez = u'Привет, Гость'
        return render.index(rez)

class main(object):
    def GET(self, name):
        i = web.input()
        #sid = i.get('sid', '')
        sid = web.cookies().get('sid')
        con = sqlite3.connect('overhead.sqlite')
        cur = con.cursor()
        sql = u"select * from auth where sesion=?"
        cur.execute(sql, (sid,))
        r = cur.fetchall()
        if r:
            rez = r[0][1]
        else:
            #pass
            raise web.redirect('/')
        web.header('Content-type', 'text/html; charset=utf-8')
        out = render.main({'name': rez, 'uuid': sid})
        #out = render.main()
        #print '1121:', out.uuid
        return out

class users(object):
    def GET(self, name):
        i = web.input()
        #sid = i.get('sid', '')
        sid = web.cookies().get('sid')
        con = sqlite3.connect('overhead.sqlite')
        cur = con.cursor()
        sql = u"select * from auth where sesion=?"
        cur.execute(sql, (sid,))
        r = cur.fetchall()
        if r:
            rez = r[0][1]
        else:
            #pass
            raise web.redirect('/')
        web.header('Content-type', 'text/html; charset=utf-8')
        out = render.users({'name': rez, 'uuid': sid})
        #print '1121:', out.uuid
        return out

class exit(object):
    def GET(self, name):
        sid = web.cookies().get('sid')
        if sid:
            con = sqlite3.connect('overhead.sqlite')
            cur = con.cursor()
            uid = uuid.uuid4()
            sql = u"UPDATE auth SET sesion=? WHERE sesion=?"
            cur.execute(sql, (uid.hex, sid))
            con.commit()
        raise web.redirect('/')


app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()
