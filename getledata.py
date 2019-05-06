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
import sys
import unicodecsv as csv

url = "https://api.finna.fi/v1/search?lookfor="
searchbase = "lautapelit"  # "lautapelit"
freepics = "&type=AllFields&field[]=publishers&field[]=year&field[]=id&field[]=subjects&field[]=images&filter[]=usage_rights_str_mv%3Ausage_F&filter[]=search_daterange_mv%3A%22%5B*%2BTO%2B1930%5D%22&sort=relevance%2Cid%20asc&limit=100&prettyPrint=false&lng=fi&page="

picurl = url + searchbase + freepics

DATAPATH = "lautapelit"
CSVSEP = ";"
QUOTE = '"'
counter = 1


def writeToCSV(filename, row):

    # from io import BytesIO
    # f = BytesIO()
    with open(filename, 'ab') as csvf:
        w = csv.writer(csvf, encoding='utf-8', delimiter=',')
        w.writerow(row)


def seekFinna(picurl, counter, page=1):

    result = urlopen(picurl).read()
    result = json.loads(result)
    result = result.get('records')

    try:
        os.remove(filukka)
    except:
        pass

    for resultSet in result:
        try:
            os.remove('kuva.jpg')
        except:
            pass
        # print resultSet
        finnaprefix = "http://www.finna.fi"
        # /Cover/Show?id=musketti.M012%3AHK19670603%3A5244&index=0&size=large
        # {'images': ['/Cover/Show?id=musketti.M012%3AHK19670603%3A5244&index=0&size=large'],
        # 'subjects': [['kissa'], ['1931']]
        # ,'id': 'musketti.M012:HK19670603:5244'}

        publisher = "-"
        if 'publishers' in resultSet:
            if len(resultSet['publishers']) > 0:
                publisher = resultSet['publishers'][0].replace(' ', '_')
                publisher = publisher.replace(':', '_')
        yearx = "uuuu"
        if 'year' in resultSet:
            yearx = resultSet['year']

        if yearx != 'uuuu' and int(yearx) <= 1930:
            pass
        else:
            continue

        title = 'notitle'
        if 'title' in resultSet:
            title = resultSet['id']

        idx = counter
        if 'id' in resultSet:
            idx = resultSet['id'].replace(':', "_")

        subjs = ""
        if 'subjects' in resultSet:
            # subjs = "|".join(resultSet['subjects'])
            for sbj in resultSet['subjects']:
                subjs = subjs + '|' + sbj[0]

        outname = yearx + "_" + idx + "_pic" + '%03d' % counter + ".jpg"
        print("Publ, year:", publisher, yearx, idx, outname)

        print resultSet

        try:
            picurl = finnaprefix + resultSet['images'][0]
            counter += 1

        except:
            print "No pictures for: " + resultSet['id'] + " skipping to next record."
            continue

        # skipping these images since they seem to require special handling.
        if ("sls.SLSA" in picurl):
            continue

        print "Pic: " + picurl
        writeToCSV(filukka, [outname, resultSet['id'],
                             picurl,  yearx, publisher, title,  subjs])
        # + "," +           resultSet['id'] + "," + yearx + "," + publisher + "," + subjs)

        # In some cases there might not be subjects words given, then use searchbase as last resort.
        try:
            subjectlist = resultSet['subjects']
        except:
            subjectlist = [searchbase]

        # in win wget has issues w filenames...
        localpic = wget.download(picurl)
        #print("!!", localpic)

        better = yearx + "_" + idx + "_pic" + '%03d' % counter + ".jpg"

        # better = os.path.join(DATAPATH, outname)

        try:
            os.rename(localpic, better)

        except:
            print("Moving file {0}->{1} failed ..".format(localpic, outname))
    return counter


result = urlopen(picurl+str(1)).read()
result = json.loads(result)

recCount = result['resultCount']
print "Tietueita löytynyt: ", str(recCount)

result = result.get('records')
filukka = "lautapelitmeta1b.csv"

# print(result)
# sys.exit(1)

rounds = (int(recCount) / 100) + 1
print str(
    result) + " tietuetta löytynyt, 100 per sivu. Tarvitaan {0} kierrosta.\n".format(rounds)
# sys.exit(1)
page = 0
while page < rounds:
    page += 1
    urli = picurl + str(page)
    #print("Seeking page: ", page, "w urili: ", urli)

    counter = seekFinna(urli, counter)
