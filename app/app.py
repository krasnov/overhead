#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '2011.0413'
print 'ver:', __version__

import web
render = web.template.render('templates/')

urls = [
    '(.*)/cdx', 'cdx',
    '(.*)', 'cdx1',
]

class cdx1(object):
    def GET(self, name):
        web.header('Content-type', 'text/html; charset=utf-8')
        i = web.input()
        if i:
            n = i.name
        else:
            n = u'Мир'
        s = u'''
<html>
<head>

</head>

<body>
<h1>Привет, %s!</h1>
</body>
</html>
        ''' % n 
        return s
        
class cdx(object):
    def GET(self, name):
        web.header('Content-type', 'text/html; charset=utf-8')
        i = web.input()
        if i:
            n = i.name
        else:
            n = u'world'
        s = u'''
<html>
<head>

</head>

<body>
<h1>Hello, %s!</h1>
</body>
</html>
        ''' % n 
        return s
app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()
