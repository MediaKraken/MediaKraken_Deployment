from common import common_file

"""
This program will be used to find all the db calls that need to be ported to asyncpg
"""

# find all sanic py files
sanic_db_files = common_file.com_file_dir_list('./web_app_sanic', '.py',
                                               walk_dir=True,
                                               skip_junk=True,
                                               file_size=False,
                                               directory_only=False, file_modified=False)

# find all async py files
async_db_files = common_file.com_file_dir_list('./database_async', '.py',
                                               walk_dir=True,
                                               skip_junk=True,
                                               file_size=False,
                                               directory_only=False,
                                               file_modified=False)

# read in all the sanic files
sanic_db_call_table = []
for sanic_file in sanic_db_files:
    print('Sanic File:', sanic_file)
    file_handle = open(sanic_file, 'r')
    for file_line in file_handle.readlines():
        # print(file_line)
        if file_line.find('request.app.db_functions.') != -1:
            db_call = file_line.split('request.app.db_functions.')[1].split('(')[0]
            if db_call in sanic_db_call_table:
                pass
            else:
                sanic_db_call_table.append(db_call)
    file_handle.close()
print('Unique Calls ', len(sanic_db_call_table), sanic_db_call_table)

# read in all the db files
async_db_call_table = []
need_to_code = sanic_db_call_table
for db_file in async_db_files:
    print('DB File:', db_file)
    file_handle = open(db_file, 'r')
    for file_line in file_handle.readlines():
        # print(file_line)
        if file_line.find('def ') != -1:
            db_call = file_line.split('def ')[1].split('(')[0]
            if db_call in async_db_call_table:
                pass
            else:
                async_db_call_table.append(db_call)
            try:
                need_to_code.remove(db_call)
            except ValueError:  # not in list
                pass
    file_handle.close()
print('Unique Calls DB', len(async_db_call_table), async_db_call_table)

print('Need to Code', len(need_to_code), sorted(need_to_code))
