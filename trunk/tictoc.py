#!/usr/bin/env python
#
# Serve TicToc records
#
# Godmar Back <libx.org@gmail.com>
# April 2009
#
import wsgiref.handlers
import urllib
import logging
import datetime, time

from django.utils import simplejson
from difflib import get_close_matches

from google.appengine.api import users, urlfetch, memcache
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template

class Configuration(db.Model):
  lastmod = db.DateTimeProperty()

configQuery = db.GqlQuery("SELECT * FROM Configuration")

class Record(db.Model):
  issn = db.StringProperty()
  rssfeed = db.TextProperty()
  title = db.TextProperty()

class TicTocHandler(webapp.RequestHandler):
  def get(self):
    return self.handle()

  def handle(self):
    issn = self.request.path.replace("/", "").replace("-", "")

    result = { 'issn' : issn, 
               'records' : [], 
               'lastmod' : time.asctime(config.lastmod.timetuple()) }

    recordbytitle = dict()
    records = db.GqlQuery("SELECT * FROM Record WHERE issn = :1", issn).fetch(10)
    for record in records:
        recordbytitle[record.title] = record

    # if a title is given, find closest match;
    # if closest match is found, return only it 
    if self.request.params.has_key('title'):
        title = self.request.params['title']
        match = get_close_matches(title, recordbytitle.keys())
        if len(match) != 0:
            records = [recordbytitle[match[0]]]

    for record in records:
        result['records'].append({ 'rssfeed' : record.rssfeed, 'title' : record.title });

    resp = simplejson.dumps(result)

    # wrap result in jsoncallback if desired
    if self.request.params.has_key('jsoncallback'):
        resp = self.request.params['jsoncallback'] + "(" + resp + ")"

    self.response.headers['Content-Type'] = 'application/javascript;charset=utf-8'
    self.response.out.write(resp)

application = webapp.WSGIApplication([
    ('/.*', TicTocHandler),
], debug=True)

def main():
  global config 
  config = configQuery.get()
  if not config:
    config = Configuration()
    config.lastmod = datetime.datetime.now()
    config.put()

  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()

