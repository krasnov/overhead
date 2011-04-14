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

        s = u'''
<html>
<head>
<title>Авторизация</title>
</head>

<body>
<form name="auth" method="get" action="">
<h1> %s!</h1>
Логин
<br>
<input type="text" name="name" value="" size="30px" />
<br>
Пароль
<br>
<input type="password" name="passw" value="" size="30px" />
<br>
<input type="submit" value="Вход"/>
</form>
</body>
</html>
        ''' % rez
        return s

class cdx(object):
    def GET(self, name):
        data = web.input()
        sid = data.get('sid', '')
        con = sqlite3.connect('overhead.sqlite')
        cur = con.cursor()
        sql = u"select * from auth where sesion=?"
        cur.execute(sql, (sid,))
        r = cur.fetchall()
        if r:
            rez = r[0][1]
        else:
            raise web.redirect('/')
        web.header('Content-type', 'text/html; charset=utf-8')
        return render.index({'name': rez, 'uuid': sid})

app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()
