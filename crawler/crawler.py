#!/usr/bin/env python
import code
import logging

from xml.etree.ElementTree import ElementTree

# This is a list of the mandatory fields outside the 
# "case-file-header" node.
_case_file_identification_fields = ["serial-number",       
                                    "registration-number",
                                    "transaction-date",
                                    ]

# This is the list of the fields inside the "case-file-header"
# section.
_case_file_header_fields = ["filing-date",
                            "registration-date",
                            "status-code",
                            "status-date",
                            "mark-id",
                            "mark-drawing-code",
                            "published-for-opposition-date",
                            "amend-to-register-date",
                            "abandonment-date",
                            "cancellation-date",
                            "republished-12c-date"
                            "domestic-rep-name",
                            "attorney-docket-number",
                            "attorney-name",
                            "principal-register-ammended-in",
                            "supplemental-register-ammended-in",
                            "trademark-in",
                            "collective-trademark-in",
                            "service-mark-in",
                            "collective-service-mark-in",
                            "collective-membership-mark-in",
                            "certification-mark-in",
                            "cancellation-pending-in",
                            "published-concurrent-in",
                            "concurrent-use-in",
                            "concurrent-use-proceeding-in",
                            "interference-pending-in",
                            "opposition-pending-in",
                            "section-12c-in",
                            "section-2f-in",
                            "section-2f-in-part-in",
                            "renewal-filed-in",
                            "section-8-filed-in",
                            "section-8-partial-accept-in",
                            "section-8-accepted-in",
                            "section-15-acknowledged-in",
                            "section-15-filed-in",
                            "supplemental-register-in",
                            "foreign-priority-in",
                            "change-registration-in",
                            "intent-to-use-in",
                            "intent-to-use-current-in",
                            "filed-as-use-application-in",
                            "amended-to-use-application-in",
                            "use-application-currently-in",
                            "amended-to-itu-application-in",
                            "filing-basis-filed-as-44d-in",
                            "amended-to-44d-application-in",
                            "filing-basis-current-44d-in",
                            "filing-basis-filed-as-44e-in",
                            "amended-to-44e-application-in",
                            "filing-basis-current-44e-in",
                            "without-basis-currently-in",
                            "filing-current-no-basis-in",
                            "color-drawing-filed-in",
                            "color-drawing-currently-in",
                            "drawing-3d-filed-in",
                            "drawing-3d-current-in",
                            "standard-characters-claimed-in",
                            "filing-basis-filed-as-66a-in",
                            "filing-basis-current-66a-in",
                            "renewal-date",
                            "law-office-assigned-location-code",
                            "current-location",
                            "location-date",
                            "employee-name",
                            ]


def extract_fields(node,fields):
    """Extracts the information from the nodes in 'fields' from the
    'node' and returns them in a hash"""
    info = {}
    for i in fields:
        n = node.find(i)
        if n is not None:
            val = n.text.strip()
            info[i] = val
    return info

def extract_case_file_statements(node):
    """Extracts all <case-file-statement> nodes from the given 'node' and
    returns them in a list of dictionaries"""
    ret = []
    if not node:
        return ret
    for i in node.findall("case-file-statement"):
        typ  = i.find("type-code").text.strip()
        text = i.find("text").text.strip()
        ret.append({'type-code': typ, 'text' : text})
    return ret

def extract_case_file_event_statements(node):
    """Extracts all <case-file-event-statement> nodes from the given 'node' and
    returns them in a list of dictionaries"""
    ret = []
    if not node:
        return ret
    for i in node.findall("case-file-event-statement"):
        code = i.find("code").text.strip()
        typ  = i.find("type").text.strip()
        desc = i.find("description-text").text.strip()
        date = i.find("date").text.strip()
        number = i.find("number").text.strip()
        ret.append({'code'   : code,
                    'type'   : typ,
                    'desc'   : desc,
                    'date'   : date,
                    'number' : number
                    })
    return ret


def parse(f):
    tree = ElementTree()
    tree.parse(f)
    count = 0
    for node in tree.findall("application-information/file-segments/action-keys/case-file"):
        # Basic unique identification information
        ident = extract_fields(node,_case_file_identification_fields)
        print ident
        # Header information
        header = extract_fields(node.find("case-file-header"),_case_file_header_fields)
        print " Headers:"
        for i,j in header.iteritems():
            print "   %-40s  %s"%(i,j)
        # Statements
        statements = extract_case_file_statements(node.find("case-file-statements"))
        print " Statements:"
        for k in statements:
            print "   - %-40s  %s"%(k['type-code'],k['text'])
        # Events
        events = extract_case_file_event_statements(node.find("case-file-event-statements"))
        print " Events:"
        for k in events:
            print "   - %4s %1s %50s %8s %3s"%(k['code'],k['type'],k['desc'],k['date'],k['number'])
            

        print 80*"="
        
if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG, format="[%(lineno)d:%(funcName)s] - %(message)s")
    parse("sample_data/daily/sample.xml")
    # parse("sample_data/daily/apc090101.xml")
