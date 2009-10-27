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
                            # Add rest of fields here: TBD
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
    

def parse(f):
    tree = ElementTree()
    tree.parse(f)
    count = 0
    for node in tree.findall("application-information/file-segments/action-keys/case-file"):
        ident = extract_fields(node,_case_file_identification_fields)
        print ident
        header = extract_fields(node.find("case-file-header"),_case_file_header_fields)
        for i,j in header.iteritems():
            print "  %-40s  %s"%(i,j)
            # if element.getchildren():
            #     for i in element.getchildren():
            #         print "" 
            #         print "  ",i.tag.strip(), i.text.strip()
            # else:
            #     print element.text.strip()

        
if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG, format="[%(lineno)d:%(funcName)s] - %(message)s")
    parse("sample_data/daily/sample.xml")
    # parse("sample_data/daily/apc090101.xml")
