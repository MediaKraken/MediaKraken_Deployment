#!/usr/bin/python
# Generate a simple web slideshow
# for use with a Chromecast.
#
# Copyright (c) 2014 by Jim Lawless
# See MIT/X11 license at
# http://www.mailsend-online.com/license2014.php
#

import os
import string

import SimpleHTTPServer
import SocketServer

delay_millis = "10000"
images = os.listdir('img')
html = ''

# Build an HTML snippet that contains
# a JavaScript list of string-literals.
for img in images:
    html = html + '\"img/' + img + '\"'
    # Place a comma on the end
    # unless this is the last item in
    # the list
    if img != images[-1]:
        html = html + ','

with open('template.htm', "r") as tplfile:
    payload = tplfile.read()

# Replace $$1 and $$2 with the delay
# in milliseconds and generated list
# of images.  Write the output to
# index.html
payload = payload.replace("$$1", delay_millis)
payload = payload.replace("$$2", html)
with open("index.html", "w") as indexfile:
    indexfile.write(payload)

# Now, start serving up pages
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", 80), Handler)
print('HTTP server running...')
httpd.serve_forever()
