#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#try:
#    import pyanisort.utilities as utilities
#except ImportError:
#    import utilities
    
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import re
import difflib
import csv
import sys
import os
import io
import copy
import errno
import logging

logger = logging.getLogger(__name__)

# Set regex to a regex string or an array of regex strings to loop through
# when creating new regex group one must be show name group two must be episode number
#(!@#$%^&*()\?<>;:'"{}[]|~`+=) all of these are valid characters on linux systems included for completion
# returns [show, ep]
def parsefilename(filename ,regex=None):
    path, file = os.path.split(filename)
    if (regex is None):
        regex = [
            "(?i)(?:[^]]*\][ _.]?)((?:(?!-?[ _.](?:En?D(?:ing)?|OP(?:ening)?|E?P?(?:isode[ _.]?)?\d{2,3}))[!@#$%^&*()\\?<>;:\'\"{}\[\]|~`+=\w\s._-])+)(?:(?!\d|En?D(?:ing)?|OP(?:ening)?|\[[\dA-F]{8}\]).)*(\d{2,3})", # Matches Show and episode (Requires Sub Group for Accuracy)
            "(?i)(?:[^]]*\][ _.]?)((?:(?!-?[ _.](?:En?D(?:ing)?|OP(?:ening)?|E?P?(?:isode[ _.]?)?\d{2,3}))[!@#$%^&*()\\?<>;:\'\"{}\[\]|~`+=\w\s._-])+)(?:(?!En?D(?:ing)?|OP(?:ening)?|\[[\dA-F]{8}\]).)*(OP(?:ening)?[ _.]?(?:\d{1,2})?|En?D(?:ing)?[ _.]?(?:\d{1,2})?)", # Matches Opening and Endings (Requires Sub Group for Accuracy)
            "(?i)((?:(?!-?[ _.](?:En?D(?:ing)?|OP(?:ening)?|E?P?(?:isode[ _.]?)?\d{2,3}))[!@#$%^&*()\\?<>;:\'\"{}\[\]|~`+=\w\s._-])+)(?:(?!\d|En?D(?:ing)?|OP(?:ening)?|\[[\dA-F]{8}\]).)*(\d{2,3})",# Matches Show and episode (Doesn't require sub group)
            "(?i)(?:[^]]*\][ _.]?)((?:(?!-?[ _.](?:En?D(?:ing)?|OP(?:ening)?|E?P?(?:isode[ _.]?)?\d{2,3}))[!@#$%^&*()\\?<>;:\'\"{}\[\]|~`+=\w\s._-])+)(?:(?!En?D(?:ing)?|OP(?:ening)?|\[[\dA-F]{8}\]).)*(OP(?:ening)?[ _.]?(?:\d{1,2})?|En?D(?:ing)?[ _.]?(?:\d{1,2})?)" # Matches Opening and Endings (Doesn't require sub group)
            ]
    else:
        if type(regex) is list:
            regex = regex
        elif type(regex) is str:
            regex = [regex]
        else:
            return [None, None]
    index = 0
    while index < len(regex):
        reg = regex[index]
        m = re.match(reg, file)
        try:
            show = m.group(1)
            ep = m.group(2)
            break
        except AttributeError as e:
            logger.debug("Regex {0}: Could not find match in file '{1}'".format(index, file))
            if index < len(regex):
                index += 1
    else:
        logger.debug("Could not find match in file '{1}'".format(reg, file))
        return [None,None]

    show = re.sub('[_.]', ' ', show)
    show = show.rstrip() # remove trailing spaces
    logger.debug("Regex {0}: Found match in file '{1}': ({2}, {3})".format(index, file, show, ep))
    return [show, ep]

# set precision to a float between 0 and 1
# root is the root tag of the xmlfile
# the closer to 0 the less precise the match
# returns [[aid, title], [aid, title] ... ]
def findshowmatches(findMatch, root, precision=.9):
    allMatches = []

    # search throuh anime subtags for a matching title
    # make an array of all the names in the anime
    # then match use the difflib library to find the closest match
    for anime in root.findall('anime'):
        titleList = [anime.get('aid'), anime ]
        # store iter for current anime
        for title in anime.iterfind('title'):
            titleList.append(title.text)
        match = difflib.get_close_matches(findMatch, titleList,
                                          cutoff=precision)
        if match:
            # use iter from before to find main title
            for title in titleList[1].iterfind('title'):
                if (title.get('type') == 'main'):
                    allMatches.append([titleList[0], title.text])
    return allMatches

# command line method to choose one value from a list
def listchoice(matchList):
    while True:
        for i in range(len(matchList)):
            print ('{0}: {1}'.format(i+1, matchList[i]))
        try:
            choice = input('Please select the correct title: ')
            choice = int(choice)
            if choice > 0 and choice <= len(matchList):
                break
            else:
                print ('Choice is not valid', sys.stderr)
        except ValueError:
            print ('Error please enter a number', sys.stderr)
    choice -= 1
    return matchList[choice]

# checks the csv file for a prefered title
# returns [aid, prefName, foundName]
def findprefname(filename, findMatch):
    try:
        with open(filename) as prefTReader:
            prefTCSVReader = csv.reader(prefTReader)
            for line in prefTCSVReader:
                if line[2] == findMatch:
                    return line
    except IOError as e:
        logger.error("IOError[{0}] in file {1}: {2}".format(e.errno, filename, e.strerror))
        raise e

'''
# saves list of prefered names to a csv file without making duplicate entries
def saveprefnames(filename, prefNameList):
    prefNameListCopy = copy.deepcopy(prefNameList)
    try:
        with open(filename, 'a', newline='') as prefTWriter, open(filename, newline='') as prefTReader:
            prefTCSVReader = csv.reader(prefTReader)
            for line in prefTCSVReader:
                i = 0
                while i < len(prefNameListCopy):
                    if line[2] == prefNameListCopy[i][2]:
                        del prefNameListCopy[i]
                        break
                    i +=1
            prefTCSVWriter = csv.writer(prefTWriter)
            prefTCSVWriter.writerows(prefNameListCopy)
    except IOError as e:
        logger.error("IOError[{0}] in file {1}: {2}".format(e.errno, filename, e.strerror))

# parses xml file for title names downloads new one if necessary
# silent skips over anything that requires user input
def generateprefnamecsv(xmlFilename, ShowList):
    try:
        xmlFileObject = utilities.openFile(xmlFilename)
    except IOError as e:
        url = 'http://anidb.net/api/animetitles.xml.gz'
        utilities.downloadFile(url, xmlFilename)
        xmlFileObject = utilities.openFile(xmlFilename)
        logger.info("'{0}' not found: downloading".format(xmlFilename))

    #open xmlfile once here for faster parsing
    tree = ET.parse(xmlFileObject)
    root = tree.getroot()
    preferedNames=[]
    for show in ShowList:
        showMatches = findshowmatches(show, root)
        if (len(showMatches) == 0):
            # check date of latest animetitles.xml.gz
            # get new one if it was not already downloaded today
            if utilities.checkFileAge(xmlFilename):
                url = 'http://anidb.net/api/animetitles.xml.gz'
                utilities.downloadFile(url, xmlFilename)
                # search through xml file again
                xmlFileObject = utilities.openFile(xmlFilename)
                tree = ET.parse(xmlFileObject)
                root = tree.getroot()
                showMatches = findshowmatches(show, root)
        #get user to pick show from list or write a warning and do nothing if silent is on
        if (len(showMatches) > 1):
            if not silent:
                print('{0} matches for show {1}'.format(
                    len(showMatches), show))
                showChoice = listchoice(showMatches)
                showChoice.append(show)
                preferedNames.append(showChoice)
                showMatches = [showChoice]
                logger.debug("{0} Matched: '{1}' with {2}".format(xmlFilename, show, showChoice))
            else:
                logger.warning("Multiple matches found for title '{0}' silent mode is on".format(title))
                showMatches = []
        elif (len(showMatches) == 1):
            showMatches[0].append(show)
            preferedNames.append(showMatches[0])
            logger.debug("{0} Matched: '{1}' with {2}".format(xmlFilename, show, showMatches[0]))
        else:
            logger.error("Anime '{0}' not found".format(show))

    return preferedNames

# Each list contains the aid, preffered title, and all files in the series
def groupanimefiles(vidFilesLoc, xmlFilename='animetitles.xml.gz',
                    csvFile='prefName.csv', silentMode=False):
    global silent
    silent = silentMode

    try:
        vidFiles = utilities.listAllfiles(vidFilesLoc)
    except IOError as e:
        logger.error("IOError[{0}] in file {1}: {2}".format(e.errno, vidFilesLoc, e.strerror))
        raise e

    # make a list of all the different tv shows names
    showNames = [] # list of show titles with duplicates
    fileInfo = [] # list of info pulled from file name
    for file in vidFiles:
        showName = parsefilename(file)
        if showName is None:
            continue

        showName.append(file)
        fileInfo.append(showName)
        showNames.append(showName[0])

    shows = set(showNames)# list of show titles without duplicates
    shows = list(shows)# convert back to list
    preferedNames=[]
    allShowsAndFiles = []

    index = 0
    # check csv file for shows
    while index < len(shows):
        # store as a list of lists for consistency with pulled matches
        try:
            showMatch = findprefname(csvFile, shows[index])
        except IOError as e:
            break
        if (showMatch is not None):
            preferedNames.append(showMatch)
            logger.debug("{0} Matched: '{1}' with {2}".format(csvFile, shows[index], showMatch))
            del shows[index]
        else:
            index += 1

    # check xml file for shows
    preferedNames += generateprefnamecsv(xmlFilename, shows)

    saveprefnames(csvFile, preferedNames)

    # group all files with show info
    for aid, prefName, originalName in preferedNames:
        animeFiles = [aid, prefName]
        for file in fileInfo:
            if file[0] == originalName:
                animeFiles.append(file[1:])
        allShowsAndFiles.append(animeFiles)
    return allShowsAndFiles
'''

