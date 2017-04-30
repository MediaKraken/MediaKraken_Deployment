#!/bin/sh

if [ ! -e isbn_hyphenate/isbn_lengthmaps.py ]
then
  echo "The file isbn_hyphenate/isbn_lengthmaps.py does not exist."
  echo "This script should be called from the base directory as bin/update_ranges.sh"
  exit 1
fi

wget -O isbn_hyphenate/RangeMessage.xml http://www.isbn-international.org/agency?rmxml=1
isbn_hyphenate/isbn_xml2py.py isbn_hyphenate/RangeMessage.xml > isbn_hyphenate/isbn_lengthmaps.py
