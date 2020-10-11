# https://nickjanetakis.com/blog/how-i-used-the-lxml-library-to-parse-xml-20x-faster-in-python

import sys

from timeit import default_timer as timer


def sample_xml(opts):
    """Return the sample XML file as a string."""
    with open('test_xml_sample.xml', opts) as xml:
        return xml.read()


# xmltodict--------------------------------------------------------------------
def parse_xmltodict():
    import xmltodict
    xml_as_string = sample_xml('r')
    timer_start = timer()
    print('[xmltodict] Starting to parse XML')
    xml_xmltodict = xmltodict.parse(xml_as_string, dict_constructor=dict)
    seconds = timer() - timer_start
    print(f'[xmltodict] Finished parsing XML in {seconds} seconds')


# etree with Python's standard library ----------------------------------------
def parse_etree_stdlib():
    import xml.etree.ElementTree as etree_stdlib
    xml_as_string = sample_xml('r')
    timer_start = timer()
    print('[etree stdlib] Starting to parse XML')
    tree = etree_stdlib.fromstring(xml_as_string)
    xml_etree_stdlib = tree.findall('./Book', {})
    seconds = timer() - timer_start
    print(f'[etree stdlib] Finished parsing XML in {seconds} seconds')


# etree with lxml -------------------------------------------------------------
def parse_etree_lxml():
    from lxml import etree as etree_lxml
    xml_as_bytes = sample_xml('rb')
    timer_start = timer()
    print('[etree lxml] Starting to parse XML')
    tree = etree_lxml.fromstring(xml_as_bytes)
    xml_etree_lxml = tree.findall('./Book', {})
    seconds = timer() - timer_start
    print(f'[etree lxml] Finished parsing XML in {seconds} seconds')


# command line arguments ------------------------------------------------------
if sys.argv[1] == 'xmltodict':
    parse_xmltodict()
elif sys.argv[1] == 'etree_stdlib':
    parse_etree_stdlib()
elif sys.argv[1] == 'etree_lxml':
    parse_etree_lxml()
else:
    print('Invalid arg, please supply: xmltodict, etree_stdlib or etree_lxml')
    sys.exit(1)
