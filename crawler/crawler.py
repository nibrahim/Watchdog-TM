#!/usr/bin/python2.6

from xml.etree.cElementTree import ElementTree

def parse(f):
    tree = ElementTree()
    tree.parse(f)
    for node in tree.findall("application-information/file-segments/action-keys/case-file"):
        print "-------------------", node,
        for element in node.getchildren():
            print element.tag.strip(),
            if element.getchildren():
                for i in element.getchildren():
                    print "" 
                    print "  ",i.tag.strip(), i.text.strip()
            else:
                print element.text.strip()

if __name__ == "__main__":
    parse("sample_data/daily/sample.xml")
    # parse("sample_data/daily/apc090101.xml")





















