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

_correspondent_fields = ["address-1",
                         "address-2",
                         "address-3",
                         "address-4",
                         "address-5"]

                         
                         
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
    _case_file_event_statement_fields = ["code","type","description-text","date","number"]
    for i in node.findall("case-file-event-statement"):
        d = extract_fields(i,_case_file_event_statement_fields)
        ret.append(d)
    return ret

def extract_prior_registration_applications(node):
    """Extracts all <prior-registration-application> nodes from the
    given 'node' and returns them in a list of dictionaries. Also gets
    nodes outside these."""
    ret = {}
    if not node:
        return ret
    other_indicator = node.find("other-related-in")
    if other_indicator:
        other_related_in = other_indicator.text.strip()
        ret['other_related_in'] = other_related_in
    prior_reg_applications = []
    _prior_registration_application_fields = ["relationship-type", "number"]
    for i in node.findall("prior-registration-application"):
        prior_reg_applications.append(extract_fields(node.find("prior-registration-application"),
                                                     _prior_registration_application_fields))
    ret['prior-registration-applications'] = prior_reg_applications
    return ret

def extract_foreign_applications(node):
    """Extracts all <foreign-application> nodes from the given 'node' and
    returns them in a list of dictionaries"""
    ret = []
    if not node:
        return ret
    _foreign_application_fields = ["filing-date",
                                   "registration-date",
                                   "registration-expiration-date",
                                   "registration-renewal-date",
                                   "registration-renewal-expiration-date",
                                   "entry-number",
                                   "application-number",
                                   "country",
                                   "other",
                                   "registration-number",
                                   "renewal-number",
                                   "foreign-priority-claim-in",
                                   ]
    for i in node.findall("foreign-application"):
        d = extract_fields(i,_foreign_application_fields)
        ret.append(d)
    return ret


def extract_classifications(node):
    """Extracts all <classification> nodes from the given 'node' and
    returns them in a list of dictionaries"""
    ret = []
    if not node:
        return ret
    _classification_fields = ["international-code-total-no",
                              "us-code-total-no",
                              "international-code",
                              "us-code",
                              "status-code",
                              "status-date",
                              "first-use-anywhere-date",
                              "first-use-in-commerce-date",
                              "primary-code",
                              ]
    for i in node.findall("classification"):
        d = extract_fields(i,_classification_fields)
        ret.append(d)
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
            print "   - %-40s  %s"%(k['type-code'],k['text'][:20]+"...")
        # Events
        events = extract_case_file_event_statements(node.find("case-file-event-statements"))
        print " Events:"
        for k in events:
            print "   - %4s %1s %50s %8s %3s"%(k['code'],k['type'],k['description-text'][:45],k['date'],k['number'])
        # Prior applications
        prior_apps = extract_prior_registration_applications(node.find("prior-registration-applications"))
        print " Prior applications:"
        if 'other_related_in' in prior_apps:
            print "   Other related indicatior  %s"%prior_apps['other_related_in']
        if 'prior-registration-applications' in prior_apps:
            for app in prior_apps['prior-registration-applications']:
                print "   |"
                for i,j in app.iteritems():
                    print "    - %-40s  %s"%(i,j)

        # Foreign applications
        foreign_applications = extract_foreign_applications(node.find("foreign-applications"))
        print " Foreign applications:"
        for k in foreign_applications:
            print "   |"
            for i,j in k.iteritems():
                print "    - %-40s  %s"%(i,j)

        # Classifications
        classifications = extract_classifications(node.find("classifications"))
        print " Classifications:"
        for k in classifications:
            print "   |"
            for i,j in k.iteritems():
                print "    - %-40s  %s"%(i,j)

        #Correspondent
        correspondent = extract_fields(node.find("correspondent"),_correspondent_fields)
        print " Correspondent:"
        for i,j in correspondent.iteritems():
            print "   %-40s  %s"%(i,j)

        print 80*"="

        
if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG, format="[%(lineno)d:%(funcName)s] - %(message)s")
    parse("sample_data/daily/sample.xml")
    # parse("sample_data/daily/apc090101.xml")
