'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
'''

# import modules
import glob
import os

master_directory = os.getcwd()
# hold all the directories to parse
dir_to_parse = []

# extentions to parse
types = ('*.mkv', '*.avi', '*.mp4', '*.mov', '*.wmv', '*.webm')

dir_to_parse.append('Beta')
dir_to_parse.append('Beta_Super')
dir_to_parse.append('BluRay')
dir_to_parse.append('BluRay_3D')
dir_to_parse.append('BluRay_Dir_Cut')
dir_to_parse.append('DVD')
dir_to_parse.append('DVD_3D')
dir_to_parse.append('DVD_Dir_Cut')
# dir_to_parse.append('DVD_Rip')
dir_to_parse.append('HDDVD')
dir_to_parse.append('Laserdisc')
dir_to_parse.append('Movie_Misc')
# dir_to_parse.append('Music_CD')
# dir_to_parse.append('Music_Video')
dir_to_parse.append('Sports_BluRay')
dir_to_parse.append('Sports_DVD')
dir_to_parse.append('Sports_Misc')
# dir_to_parse.append('TV_Shows_BluRay')
# dir_to_parse.append('TV_Shows_DVD')
dir_to_parse.append('VHS')
dir_to_parse.append('VHS_Super')

# loop through the directories looking for media files
for directory_local in dir_to_parse:
    os.chdir(master_directory + directory_local)
    # populate from multiple globs
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))
    # parse the results
    for file in files_grabbed:
        print(file)
        new_dir_name = file.rsplit('.', 1)[0]
        file_extension = extension = os.path.splitext(file)[1]
        if new_dir_name.find('_') == -1:
            pass
        else:
            old_dir_name = new_dir_name
            new_dir_name = new_dir_name.replace('_', ' ')
            command_to_run = 'mv ' + master_directory + directory_local + "/\"" \
                             + old_dir_name + '.' + file_extension + '\" ' \
                             + master_directory + directory_local + "/\"" \
                             + new_dir_name + "." + file_extension + "\""
            print(command_to_run)
            os.system(command_to_run)
        print(os.path.join(master_directory, directory_local, new_dir_name))
        if not os.path.exists(os.path.join(master_directory, directory_local, new_dir_name)):
            # create the directory for the video files
            os.mkdir(os.path.join(master_directory, directory_local, new_dir_name))
            # create the directory for the trailer files
            os.mkdir(os.path.join(master_directory, directory_local, new_dir_name, "trailers"))
            # create the directory for the chapter files
            os.mkdir(os.path.join(master_directory, directory_local, new_dir_name, "chapters"))
            # create the directory for the extras files
            os.mkdir(os.path.join(master_directory, directory_local, new_dir_name, "extras"))
            # create the directory for the theme music files
            os.mkdir(os.path.join(master_directory, directory_local, new_dir_name, "theme-music"))
            # create the directory for the theme video/etc files
            os.mkdir(os.path.join(master_directory, directory_local, new_dir_name, "backdrops"))
            # move the corresponding files and metadata
            command_to_run = 'mv ' + master_directory + directory_local + "/\"" \
                             + new_dir_name + '\".* ' \
                             + master_directory + directory_local + "/\"" + new_dir_name + "\"/."
            print(command_to_run)
            os.system(command_to_run)
            command_to_run = 'mv ' + master_directory + directory_local + "/\"" \
                             + new_dir_name + '-\"* ' \
                             + master_directory + directory_local + "/\"" + new_dir_name + "\"/."
            print(command_to_run)
            os.system(command_to_run)
            # change overship of files
            command_to_run = 'chown -R spoot: \"' + os.path.join(master_directory, directory_local,
                                                                 new_dir_name) + '\"'
            print(command_to_run)
            os.system(command_to_run)
            # change rights just in case of files
            command_to_run = 'chmod -R 755 \"' + os.path.join(master_directory, directory_local,
                                                              new_dir_name) + '\"'
            print(command_to_run)
            os.system(command_to_run)

'''
# setup the music video files
# loop through the dirctories looking for media files
directory_local = "Music_Video"
os.chdir(master_directory + directory_local)
# populate from multiple globs
allFiles = os.listdir(master_directory + directory_local)
for file in allFiles:
    # parse the results
    print(file)
    if not os.path.isdir(file):
        new_dir_name = file.rsplit('-',1)[0].strip()
        print "zui:",new_dir_name
        if not os.path.exists(master_directory + directory_local + "/" + new_dir_name):
            print "what",new_dir_name
            # create the directory for the video files
            os.mkdir(os.path.join(master_directory, directory_local, new_dir_name))
        # move the corresponding files and metadata
        command_to_run = 'mv ' + master_directory + directory_local + "/\"" + new_dir_name + '\".* ' + master_directory + directory_local + "/\"" + new_dir_name + "\"/."
        print command_to_run
        os.system(command_to_run)
        command_to_run = 'mv ' + master_directory + directory_local + "/\"" + new_dir_name + '\"* ' + master_directory + directory_local + "/\"" + new_dir_name + "\"/."
        print command_to_run
        os.system(command_to_run)
        # change overship of files
        command_to_run = 'chown -R spoot: \"' + os.path.join(master_directory, directory_local,
         new_dir_name) + '\"'
        print command_to_run
        os.system(command_to_run)
        # change rights just in case of files
        command_to_run = 'chmod -R 755 \"' + os.path.join(master_directory, directory_local,
         new_dir_name) + '\"'
        print command_to_run
        os.system(command_to_run)
'''
