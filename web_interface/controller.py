#!/usr/bin/env python
import web
import codes

urls = (
    r'/', 'index'
)

web.config.debug = True
app = web.application(urls, globals(), autoreload = True)
render = web.template.render('templates/')
db = web.database(dbn="postgres", user = "noufal", db="watchdog")

def process(row):
    """Expands all symbolic codes in the given row to proper values"""
    for field,val in row.items():
        row[field] = codes.translate(field,val)
    return row
                                 
class index:
    def GET(self):
        i = web.input(rno = False,sno = False)
        rno, sno = i['rno'], i['sno']
        assert (sno or rno) # Must provide atleast one
        assert not (sno and rno) # Can't provide both
        if sno:
            d = dict(serial_number = sno)
            tminfo = db.where('trademarks', **d)
        if rno:
            d = dict(registration_number = rno)
            tminfo = db.where('trademarks', **d)
        if not tminfo:
            tminfo = []
        else:
            tminfo = tminfo[0]
            serial_number = tminfo['serial_number']
        tminfo = process(tminfo)
        return render.index(tminfo)

if __name__ == "__main__":
    app.run()
