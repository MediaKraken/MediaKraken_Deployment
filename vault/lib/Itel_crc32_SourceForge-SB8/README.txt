to create the crc application using the cl compiler run

cl -c /O2 crc.c
cl -c /O2 8x256_tables.c
cl crc.obj 8x256_tables.obj -o crc.exe 