try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

count = 0
for event, elem in ET.iterparse('/mediakraken/emulation/mame0224.xml', events=("end",)):
    if event == "end":
        if elem.tag == 'machine':  # and elem.text and 'Africa' in elem.text:
            count += 1
            # end, name row from xml file
            elem_data = elem.attrib  # it's a DICT at this point
            print(event, elem_data)
            print(elem_data['name'])

            # data = elem.attrib.items()
            # print(data['name'])
            elem_child = list(elem)  # getchildren is depreciated
            print(elem_child)
            for child in elem_child:
                print(child.itertext())
                print(child.tag, child.items())

            # for child in elem_child:
            #     print(child.itertext())  # prints blank atm
            #     print(child.items())  # element iterator
            #     print(child.keys())  # blank atm
        elem.clear()

print('count =', count)
