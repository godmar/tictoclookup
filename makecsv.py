#!/usr/bin/python
#
# Preprocess TicToc file for import into Google AppEngine
#
import sys
import csv, urllib, os, time
from StringIO import StringIO

data = dict()
writer = csv.writer(open("out.csv", "w"))
tictocfile = urllib.urlopen(sys.argv[1])
for line in csv.reader(tictocfile, delimiter = '\t'):
    for issn in list(set(line[3:])):
        if issn.strip() != "":
            issn = issn.replace("-", "")
            key = issn + line[1]
            if data.has_key(key):
                print "found duplicate ISSN+name ", " ".join(line)
                if line[2] != data[key]:
                    print " -> warning, two entries have different feeds: ", line[2], "!=", data[key]
            else:
                data[key] = line[2]
                writer.writerow([issn, line[1], line[2]])
    
