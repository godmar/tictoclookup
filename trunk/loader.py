#!/usr/bin/env python
#
# Load preprocess TicToc records into GAE
# assume input is CSV
# (issn, title, rssfeedurl)
#
# Author: Godmar Back libx.org@gmail.com
#
import hashlib

from google.appengine.ext import db, webapp
from google.appengine.tools import bulkloader

class Record(db.Model):
  issn = db.StringProperty()
  rssfeed = db.TextProperty()
  title = db.TextProperty()

class RecordLoader(bulkloader.Loader):
  def __init__(self):
    bulkloader.Loader.__init__(self, 'Record',
        [('issn', str),
         ('title', lambda x : x.decode('utf8')),
         ('rssfeed', lambda x : x.decode('utf8')),
        ])

  def generate_key(self, lineno, values):
    issn = values[0] 
    title = values[1]
    sha1 = hashlib.sha1()
    sha1.update(title)
    # must start with a letter
    return 'key-' + issn + '-' + sha1.hexdigest()

loaders = [RecordLoader]

