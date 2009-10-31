#!/usr/bin/env python
import code
import logging

import web 
import psycopg2

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
                            "mark-identification",
                            "mark-drawing-code",
                            "published-for-opposition-date",
                            "amend-to-register-date",
                            "abandonment-date",
                            "cancellation-date",
                            "republished-12c-date",
                            "domestic-rep-name",
                            "attorney-docket-number",
                            "attorney-name",
                            "principal-register-amended-in",
                            "supplemental-register-amended-in",
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

_international_registration_fields = ["international-registration-number",
                                      "international-registration-date",
                                      "international-publication-date",
                                      "international-renewal-date",
                                      "auto-protection-date",
                                      "international-death-date",
                                      "international-status-code",
                                      "international-status-date",
                                      "priority-claimed-in",
                                      "priority-claimed-date",
                                      "first-refusal-in",
                                      ]

def extract_fields(node, fields, debug = False):
    """Extracts the information from the nodes in 'fields' from the
    'node' and returns them in a hash"""
    info = {}
    if not node:
        return info
    for i in fields:
        if debug: print i
        n = node.find(i)
        val = ''
        if n is not None:
            val = n.text.strip()
        # Sane values for date field value if it's invalid or
        # nonexistent in the XML file.
        if debug:
            print " val before cleaning is ", val
        if i.endswith("-date"):
            if not val or (n.text and n.text.strip() == '0'):
                val = "15000101"
        if debug:
            print " Storing '%s' as '%s'"%(val,i.replace("-","_"))
        info[i.replace("-","_")] = val
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
        ret.append({'type_code': typ, 'text' : text})
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
    if other_indicator is not None:
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

def extract_case_file_owners(node):
    """Extracts all <case-file-owner> nodes from the given 'node' and
    returns them in a list of dictionaries"""
    ret = []
    if not node:
        return ret
    _case_file_owner_fields = ["entry-number",
                               "party-type",
                               # "nationality" # Extracted manually since it's composite
                               "legal-entity-type-code",
                               "entity-statement",
                               "party-name",
                               "address-1",
                               "address-2",
                               "city",
                               "state",
                               "country",
                               "other",
                               "postcode",
                               "dba-aka-text",
                               "composed-of-statement",
                               "name-change-explanation",
                               ]
    for i in node.findall("case-file-owner"):
        d0 = extract_fields(i,_case_file_owner_fields)
        d1 = extract_fields(i.find("nationality"),["state","country","other"])
        for key,val in d1.iteritems(): # Flattening out the nationality node into the top level one
            d0["nationality_%s"%key] = val
        ret.append(d0)
    return ret


def extract_design_searches(node):
    """Extracts all <design-search> nodes from the given 'node' and
    returns them in a list of dictionaries"""
    ret = []
    if not node:
        return ret
    _design_search_fields = ["code"]
    for i in node.findall("design-search"):
        d = extract_fields(i,_design_search_fields)
        ret.append(d)
    return ret


def extract_madrid_international_filing_record(node):
    """Extracts all <madrid-international-filing-record> nodes from the given 'node' and
    returns them in a list of dictionaries"""
    ret = []
    if not node:
        return ret
    _top_level_madrid_international_filing_record_fields = ["entry-number",
                                                            "reference-number",
                                                            "original-filing-date-uspto",
                                                            "international-registration-number",
                                                            "international-status-code",
                                                            "international-status-date",
                                                            "irregularity-reply-by-date",
                                                            "international-renewal-date"
                                                            ]
    _madrid_history_events_fields = ["code","date","description-text","entry-number"]
    for i in node.findall("madrid-international-filing-record"):
        d = extract_fields(i,_top_level_madrid_international_filing_record_fields)
        d['madrid_history_events'] = []
        for j in i.findall("madrid-history-events/madrid-history-event"):
            d['madrid_history_events'].append(extract_fields(j,_madrid_history_events_fields))
        ret.append(d)
    return ret
                                                            
    

def parse_and_insert(f):
    db = web.database(dbn="postgres", user = "noufal", db="watchdog")
    tree = ElementTree()
    tree.parse(f)
    for action_key_node in tree.findall("application-information/file-segments/action-keys"):
        action_key = action_key_node.find("action-key").text.strip()
        print "Action key is %s"%action_key
        rows = []
        for node in action_key_node.findall("case-file"):
            # Basic unique identification information
            header = extract_fields(node,_case_file_identification_fields)
            header['action_key'] = action_key
            serial_number = header["serial_number"]
            print "\n ",serial_number,
            # Header information
            header.update(extract_fields(node.find("case-file-header"),_case_file_header_fields))
            print ".",
            db.insert('trademarks', seqname = False, **header)
            # Statements
            statements = extract_case_file_statements(node.find("case-file-statements"))
            print ".",
            for i in statements:
                i['tm'] = serial_number
                db.insert('case_file_statements', seqname = False, **i)
            # Events
            events = extract_case_file_event_statements(node.find("case-file-event-statements"))
            print ".",
            for i in events:
                i["tm"] = serial_number
                db.insert('case_file_event_statements', seqname = False, **i)
            # Prior applications
            prior_apps = extract_prior_registration_applications(node.find("prior-registration-applications"))
            if 'other_related_in' in prior_apps:
                print ",",
                db.update('trademarks', where = "serial_number = $serial_number",
                          vars = dict(serial_number = serial_number),
                          other_related_in = prior_apps['other_related_in']
                          )
            if 'prior-registration-applications' in prior_apps:
                print ".",
                for i in prior_apps['prior-registration-applications']:
                    i['tm'] = serial_number
                    db.insert('prior_registration_applications', seqname = False, **i)
            # Foreign applications
            foreign_applications = extract_foreign_applications(node.find("foreign-applications"))
            print ".",
            for i in foreign_applications:
                   i['tm'] = serial_number
                   db.insert('foreign_applications', seqname = False, **i)
                   
            # Classifications
            classifications = extract_classifications(node.find("classifications"))
            print ".",
            for i in classifications:
                i['tm'] = serial_number
                db.insert('classifications', seqname = False, **i)

            #Correspondent
            correspondent = extract_fields(node.find("correspondent"),_correspondent_fields)
            print ".",
            correspondent['tm'] = serial_number
            db.insert('correspondent', seqname = False, **correspondent)

            # # Case file owners
            case_file_owners = extract_case_file_owners(node.find("case-file-owners"))
            print ".",
            for i in case_file_owners:
                i['tm'] = serial_number
                db.insert('case_file_owners', seqname = False, **i)

            # Design searches
            design_searches = extract_design_searches(node.find("design-searches"))
            print ".",
            for i in design_searches:
                i['tm'] = serial_number
                db.insert('design_searches', seqname = False, **i)

            # International registration
            international_registration = extract_fields(node.find("international-registration"),_international_registration_fields)
            international_registration['tm'] = serial_number
            db.insert("international_registrations", seqname = False, **international_registration)

            # Madrid international filing records
            madrid_international_filing_records = extract_madrid_international_filing_record(node.find("madrid-international-filing-requests"))
            print ".",
            for i in madrid_international_filing_records:
                try:
                    i['tm'] = serial_number
                    history_events = i['madrid_history_events']
                    del i['madrid_history_events'] # Keep this aside since we're not inserting it
                    db.insert('madrid_international_filing_records', seqname = False, **i)
                    for j in history_events:
                        j['filing_record'] = i['reference_number'] # Foreign key for history events table
                        db.insert('madrid_history_events', seqname = False, **j)
                except psycopg2.IntegrityError:
                    print "Skipping one madrid update ", i
                
if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG, format="[%(lineno)d:%(funcName)s] - %(message)s")
    # parse_and_insert("sample_data/daily/sample.xml")
    parse_and_insert("sample_data/daily/apc090101.xml")
