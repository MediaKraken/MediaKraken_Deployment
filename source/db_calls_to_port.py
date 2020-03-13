import os

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
init_dict = {}
for db_file in async_db_files:
    print('DB File:', db_file)
    if os.path.basename(db_file) != '__init__.py':
        file_handle = open(db_file, 'r')
        db_file_call = []
        for file_line in file_handle.readlines():
            # print(file_line)
            if file_line.find('def ') != -1:
                db_call = file_line.split('def ')[1].split('(')[0]
                if db_call in db_file_call:
                    pass
                else:
                    db_file_call.append(db_call)
                if db_call in async_db_call_table:
                    pass
                else:
                    async_db_call_table.append(db_call)
                try:
                    need_to_code.remove(db_call)
                except ValueError:  # not in list
                    pass
        file_handle.close()
        init_dict[db_file] = db_file_call
print('Unique Calls DB', len(async_db_call_table), async_db_call_table)

print('Need to Code', len(need_to_code), sorted(need_to_code))

# generate the init file
file_handle = open('./database_async/__init__.py', 'w')
file_handle.write('class MKServerDatabaseAsync:\n')
file_handle.write('    """\n')
file_handle.write('    Main database class for async database access\n')
file_handle.write('    """\n')
for file_name in init_dict.keys():
    if len(init_dict[file_name]) > 0:
        first_record = True
        file_handle.write(
            '    from database_async.%s \\\n' % os.path.basename(file_name).split('.py')[0])
        db_call_count = 0
        for db_call in init_dict[file_name]:
            db_call_count += 1
            if first_record:
                first_record = False
                if db_call_count == len(init_dict[file_name]):
                    file_handle.write('        import %s\n' % db_call)
                else:
                    file_handle.write('        import %s, \\\n' % db_call)
            else:
                if db_call_count == len(init_dict[file_name]):
                    file_handle.write('        %s\n' % db_call)
                else:
                    file_handle.write('        %s, \\\n' % db_call)
file_handle.close()
