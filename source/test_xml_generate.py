# https://nickjanetakis.com/blog/how-i-used-the-lxml-library-to-parse-xml-20x-faster-in-python

import random
import string

from timeit import default_timer as timer

timer_start = timer()

print('Starting to write ~250mb XML file')

with open('test_xml_sample.xml', 'w') as xml:
    books = ''
    for _ in range(2000000):
        title = ''.join(random.choices(string.ascii_uppercase, k=16))
        first_name = ''.join(random.choices(string.ascii_lowercase, k=8))
        last_name = ''.join(random.choices(string.ascii_lowercase, k=12))
        alive = random.choice(['yes', 'no'])
        books += f'''
    <Book>
        <Title>{title}</Title>
        <Author alive="{alive}" />{first_name} {last_name}</Author>
    </Book>'''
    content = f'''<?xml version="1.0" encoding="utf-8"?>
<Catalog>{books}
</Catalog>
'''

    xml.write(content)

seconds = timer() - timer_start

print(f'Finished writing ~250mb XML file in {seconds} seconds')
