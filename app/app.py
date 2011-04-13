#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '2011.0413'
print 'ver:', __version__

import sqlite3
import web
render = web.template.render('templates/')

urls = [
    '(.*)/cdx', 'cdx',
    '(.*)', 'cdx1',
]

class cdx1(object):
    def GET(self, name):
        web.header('Content-type', 'text/html; charset=utf-8')
        con = sqlite3.connect('overhead.sqlite')
        cur = con.cursor()
        i = web.input()
        if i:
            n = i.name
            p = i.passw
            sql = u"select * from auth where user=? and passw=?"
            cur.execute(sql, (n, p))
            r = cur.fetchall()
            if r:
                global rez
                rez = r[0][1]
                raise web.redirect('/cdx')
            else:
                rez = u'Нет таких'
        else:
            rez = u'Привет, Гость'


        s = u'''
<html>
<head>

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
        web.header('Content-type', 'text/html; charset=utf-8')
        #raise web.redirect('/')
        s = u'''
<html>
<head>

</head>

<body>
<h1>Привет, %s!</h1>
</body>
</html>
        ''' % rez
        return s
app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()
