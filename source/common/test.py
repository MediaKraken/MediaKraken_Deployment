import chardet
import cchardet

a = '\u00FC'

encoding = chardet.detect(a)
print encoding


print a.decode('utf-16')
