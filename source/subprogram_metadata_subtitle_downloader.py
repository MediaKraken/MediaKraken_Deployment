
# parse arguments
sub_lang = "en"
# loop through all the libraries
for lib_row in db_connection.db_library_paths():
    # search the directory for filter files
    for media_row in common_file.com_file_dir_list(lib_row['mm_media_dir_path'],
                                                   ('avi', 'mkv', 'mp4', 'm4v'), True):
        # run the subliminal fetch for episode
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'title check': media_row.rsplit(
                '.', 1)[0] + "." + sub_lang + ".srt"})
        # not os.path.exists(media_row.rsplit('.',1)[0] + ".en.srt")
        # and not os.path.exists(media_row.rsplit('.',1)[0] + ".eng.srt")
        if not os.path.exists(media_row.rsplit('.', 1)[0] + "." + sub_lang + ".srt"):
            # change working dir so srt is saved in the right spot
            total_download_attempts += 1
            os.chdir(media_row.rsplit('/', 1)[0])
            file_handle = subprocess.Popen(shlex.split(
                "subliminal -l " + sub_lang + " -- \"" + media_row + "\""),
                stdout=subprocess.PIPE, shell=False)
            cmd_output = file_handle.communicate()[0]
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
                'Download Status': cmd_output})

# TODO put in the notifications
print(('Total subtitle download attempts: %s' % total_download_attempts), flush=True)

# close DB
db_connection.db_close()
