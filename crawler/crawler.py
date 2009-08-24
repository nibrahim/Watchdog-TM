#!/usr/bin/python2.6

from xml.etree.cElementTree import ElementTree

def parse(f):
    tree = ElementTree()
    tree.parse(f)
    m = tree.findall("application-information/file-segments/action-keys/case-file")
    print m

if __name__ == "__main__":
    # parse("sample_data/daily/sample.xml")
    parse("sample_data/daily/apc090101.xml")
