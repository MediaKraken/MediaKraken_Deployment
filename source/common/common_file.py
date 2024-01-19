import os
import time

image_dir = [
    'backdrop',
    'banner',
    'box_bluray',
    'box_cd',
    'box_dvd',
    'box_hddvd',
    'box_laserdisc',
    'box_uhd',
    'box_vhs',
    'chapter',
    'character',
    'fanart',
    'game',
    'game_box',
    'game_media',
    'logo',
    'media_bluray',
    'media_cd',
    'media_dvd',
    'media_hddvd',
    'media_laserdisc',
    'media_uhd',
    'media_vhs',
    'person',
    'poster',
    'profile',
    'still',
    'episodes',
]

JUNK_FILES = [
    '(gameplay)',
    'official gameplay',
    'movie clip',
    'fan made',
    'review -',
    'full movie',
    'full album',
    'full length',
    'deleted scene',
]

trailer_dir = [
    'trailer',
    'behind',
    'clip',
    'carpool',
    'featurette',
]


def com_file_build_image_dirs():
    for image_info in image_dir:
        for ndx in ascii_lowercase:
            for ndx2 in ascii_lowercase:
                os.makedirs(os.path.join(common_global.static_data_directory + '/meta/images',
                                         image_info, ndx, ndx2), exist_ok=True)


def com_file_build_trailer_dirs():
    for trailer_info in trailer_dir:
        for ndx in ascii_lowercase:
            for ndx2 in ascii_lowercase:
                os.makedirs(os.path.join(common_global.static_data_directory + '/meta/trailers',
                                         trailer_info, ndx, ndx2), exist_ok=True)


def com_file_modification_timestamp(file_name):
    """
    Return file modification date in datetime format
    """
    # do try except as it'll lessen the fs calls to one
    try:
        return os.path.getmtime(file_name)
    except FileNotFoundError:
        return None


def com_file_save_data(file_name, data_block, as_pickle=False,
                       with_timestamp=False,
                       file_ext=None):
    """
    Save data as file
    """
    if as_pickle:
        write_type = 'wb'
    else:
        write_type = 'w+'
    if with_timestamp:
        file_handle = open(os.path.join(file_name, '_', time.strftime("%Y%m%d%H%M%S"), file_ext),
                           write_type)
    else:
        file_handle = open(file_name, write_type)
    if as_pickle:
        pickle.dump(data_block, file_handle)
    else:
        file_handle.write(data_block)
    file_handle.close()


def com_file_load_data(file_name, as_pickle=False):
    """
    Load data from file as ascii or pickle
    """
    if as_pickle:
        read_type = 'rb'
    else:
        read_type = 'r'
    file_handle = open(file_name, read_type)
    if as_pickle:
        data_block = pickle.loads(file_handle.read())
    else:
        data_block = file_handle.read()
    file_handle.close()
    return data_block


def com_file_dir_list_dict(dir_name, file_modified=False):
    """
    Find all files in dir with less "rules"
    """
    match_dict = {}
    for file_name in os.listdir(dir_name):
        match_dict[os.path.basename(file_name) + '.zip'] = com_file_modification_timestamp(
            file_name)


def com_file_dir_list(dir_name, filter_text=None, walk_dir=None, skip_junk=True,
                      file_size=False, directory_only=False, file_modified=False):
    """
    Find all filtered files in directory
    """
    if os.path.isdir(dir_name):
        match_list = []
        if not walk_dir:
            if filter_text is not None:
                for file_name in os.listdir(dir_name):
                    # filter text such as '.txt'
                    if file_name.endswith(filter_text):
                        match_list.append(os.path.join(dir_name, file_name))
            else:
                for file_name in os.listdir(dir_name):
                    if directory_only:
                        if os.path.isdir(os.path.join(dir_name, file_name)):
                            match_list.append(
                                os.path.join(dir_name, file_name))
                    else:
                        match_list.append(os.path.join(dir_name, file_name))
        else:
            for root, dirs, files in walk(dir_name):  # pylint: disable=W0612
                for file_name in files:
                    if filter_text is not None:
                        if file_name.endswith(filter_text):
                            match_list.append(os.path.join(root, file_name))
                    else:
                        if directory_only:
                            if os.path.isdir(os.path.join(dir_name, file_name)):
                                match_list.append(
                                    os.path.join(dir_name, file_name))
                        else:
                            match_list.append(os.path.join(root, file_name))
        if skip_junk and len(match_list) > 0:
            match_list = com_file_remove_junk(match_list)
        if file_size:
            match_list_size = []
            for row_data in match_list:
                if file_modified:
                    match_list_size.append((row_data,
                                            common_string.com_string_bytes2human(
                                                os.path.getsize(row_data))))
                else:
                    match_list_size.append((row_data,
                                            common_string.com_string_bytes2human(
                                                os.path.getsize(row_data)),
                                            com_file_modification_timestamp(row_data)))
            return match_list_size
        if file_modified:
            match_list_modified = []
            for row_data in match_list:
                match_list_modified.append((row_data,
                                            com_file_modification_timestamp(row_data)))
            return match_list_modified
        else:
            return match_list
    else:
        return None


def com_file_remove_junk(file_list):
    """
    Throw out junk entries in files list
    """
    for file_name in file_list:
        for search_string in JUNK_FILES:
            try:
                if file_name.lower().find(search_string) != -1:
                    file_list.remove(file_name)
                    break
            except:
                pass
    return file_list


def com_file_is_junk(file_name):
    """
    See if file is junk
    """
    for search_string in JUNK_FILES:
        try:
            if file_name.lower().find(search_string) != -1:
                return True
        except:
            pass
    return False


def com_mkdir_p(filename):
    """
    create directory path if not exists
    """
    try:
        folder = os.path.dirname(filename)
        if not os.path.exists(folder):
            os.makedirs(folder)
        return True
    except:
        return False
