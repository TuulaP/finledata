#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Experimental script to download images with given 'searchbase' word and free to use rights from finna.
# Downloads the image and creates and copies it to one or more folders based on keywords (subjects) given to image

import simplejson as json
import wget
import os
import re
from shutil import copy2
from urllib import urlopen

url = "https://api.finna.fi/v1/search?lookfor="
searchbase = "kissat"
freepics = "&type=AllFields&field[]=id&field[]=subjects&field[]=images&filter[]=usage_rights_str_mv%3Ausage_B&sort=relevance%2Cid%20asc&page=1&limit=20&prettyPrint=false&lng=fi"

picurl = url + searchbase + freepics

DATAPATH = "Z:\\finnakuvadata"

CSVSEP = ";"
QUOTE  = '"'

result = urlopen(picurl).read()
result = json.loads(result)
result = result.get('records')


for resultSet in result:

    ##print resultSet
    finnaprefix = "http://www.finna.fi"
    #/Cover/Show?id=musketti.M012%3AHK19670603%3A5244&index=0&size=large
    #{'images': ['/Cover/Show?id=musketti.M012%3AHK19670603%3A5244&index=0&size=large'],
    # 'subjects': [['kissa'], ['1931']]
    #,'id': 'musketti.M012:HK19670603:5244'}

    ##print resultSet['images'][0]

    try:
        picurl = finnaprefix  + resultSet['images'][0]
    except:
        print "No pictures for: " + resultSet['id'] + " skipping to next record."
        continue

    #skipping these images since they seem to require special handling.
    if ("sls.SLSA" in picurl):
        continue

    print "Pic: " + picurl


    #In some cases there might not be subjects words given, then use searchbase as last resort.
    try:
        subjectlist =  resultSet['subjects']
    except:
        subjectlist = [searchbase]


    localpic = wget.download(picurl,DATAPATH)

    regnumber = re.compile(r'^[\d\.]+$')

    for subj in subjectlist:
        picsubject = subj[0]
        #todo regex
        picsubject = re.sub(r"[\n\t\\\/\]\[\)\(]","",picsubject)
        picsubject = picsubject.replace("       ","")

        print localpic + ";Subject is: " + picsubject

        #todo. should the date-based folders removed?
        #if regnumber.match(picsubject):
        #    #print("only numbers"
        #    pass
        #else:
            #print("")

        subjfolder = DATAPATH+ "\\" + picsubject

        try:
            os.mkdir(subjfolder)
        except:
            pass

        copy2(localpic,subjfolder)



    os.remove(localpic)




