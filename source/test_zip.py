import zipfile

zip_handle = zipfile.ZipFile('c:/users/spoot/Downloads/mame0225lx.zip', 'r')  # issues if u do RB
zip_handle.extractall('c:/users/spoot/Downloads')
zip_handle.close()

