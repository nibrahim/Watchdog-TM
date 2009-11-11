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

def expand_codes(row):
    """Expands all symbolic codes in the given row to proper values"""
    for field,val in row.items():
        row[field] = codes.translate(field,val)
    return row

def get_case_file_statements(sno):
    """Return a nice summary for all the case_file_statements for the
    case with the given serial number."""
    d = dict(tm = sno)
    cfs = db.where('case_file_statements', **d)
    ret = []
    for i in cfs:
        ret.append(i['text'])
    return ret
    

def get_case_file_event_statements(sno):
    """Return a nice summary for all the case_file_statements for the
    case with the given serial number."""
    d = dict(tm = sno)
    cfs = db.where('case_file_event_statements', **d)
    ret = []
    for i in cfs:
        ret.append(i['description_text'])
    return ret

                                 
class index:
    def GET(self):
        i = web.input(rno = False,sno = False)
        rno, sno = i['rno'], i['sno']
        assert (sno or rno) # Must provide atleast one
        assert not (sno and rno) # Can't provide both
        # Get the right row based on what we have.
        if sno:
            d = dict(serial_number = sno)
            tminfo = db.where('trademarks', **d)
        if rno:
            d = dict(registration_number = rno)
            tminfo = db.where('trademarks', **d)
        if not tminfo:
            tminfo = {}
            cfs = []
            cfes = []
        else:
            tminfo = tminfo[0]
            serial_number = tminfo['serial_number']
            # Get information from other tables
            cfs  = get_case_file_statements(serial_number)
            cfes = get_case_file_event_statements(serial_number)
        tminfo = expand_codes(tminfo)
        return render.index(tminfo, cfs, cfes)


if __name__ == "__main__":
    app.run()
