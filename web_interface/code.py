
# web.py imports
import web
import web.db as db

urls = (
    r'/', 'index'
)

web.config.debug = True
app = web.application(urls, globals())
render = web.template.render('templates/')
db = web.database(dbn="postgres", user = "noufal", db="watchdog")

class index:
    def GET(self):
        i = web.input(rno = False,sno = False)
        rno, sno = i['rno'], i['sno']
        assert (sno or rno) # Must provide atleast one
        assert not (sno and rno) # Can't provide both
        if sno:
            d = dict(serial_number = sno)
            s = db.where('trademarks', **d)
        if rno:
            d = dict(registration_number = rno)
            s = db.where('trademarks', **d)
        return render.index(s)

if __name__ == "__main__":
    app.run()
