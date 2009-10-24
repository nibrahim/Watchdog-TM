#!/usr/bin/env python

from xml.etree.cElementTree import ElementTree

def extract_header_information(node):
    info = {}
    for i in ["serial-number",
              "registration-number",
              "transaction-date"]:
        print " Node being checked is ",node
        print " Looking for ",i
        n = node.find(i)
        print " Found ",n," Asserting"
        assert n
        val = n.text.strip()
        info[i] = val
    return info
    

def parse(f):
    tree = ElementTree()
    tree.parse(f)
    count = 0
    for node in tree.findall("application-information/file-segments/action-keys/case-file"):
        print "Node outside ", node
        serial_number = node.find("serial-number").text.strip()
        print serial_number
        header = extract_header_information(node)
        
            # if element.getchildren():
            #     for i in element.getchildren():
            #         print "" 
            #         print "  ",i.tag.strip(), i.text.strip()
            # else:
            #     print element.text.strip()

        
if __name__ == "__main__":
    parse("sample_data/daily/sample.xml")
    # parse("sample_data/daily/apc090101.xml")
