#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import logging
import urllib
import hashlib
import base64
 
from google.appengine.api import memcache # Cache!
from google.appengine.api import taskqueue # Queue Worker to extract the images...

from scraper import make_scraper

class MainHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.get("url", ''):
            url = urllib.unquote(self.request.get("url", ''))
            hsh = hashlib.sha1(url).hexdigest()
            img = memcache.get(hsh)
            if img is not None:
                self.response.out.write(img)
            else :
                taskqueue.add(url='/worker', params={'url': self.request.get("url", '')})
                self.response.out.write('http://' + self.request.host  + '/r/' + hsh)
        else:
            self.redirect('http://blog.superfeedr.com/image-extrator/')


class ExtractWorker(webapp2.RequestHandler):
    def post(self): # should run at most 1/s
        url = urllib.unquote(self.request.get("url", ''))
        hsh = hashlib.sha1(url).hexdigest()
        h = make_scraper(url)
        img = h.largest_image_url()
        logging.info('Image for %s found: %s', url, img)
        if img is None:
            # We want to set a value anyway... to avoid people asking for that url again over and over.
            memcache.set(hsh, "", 86400)        
        else:
            memcache.set(hsh, img, 86400)        


class RedirectHandler(webapp2.RequestHandler):
    def get(self, hsh):
        img = memcache.get(hsh)
        if img is not None:
          if img is not "":
            self.redirect(img.encode('ascii','ignore'))
          else:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=='))
        else :
          self.response.headers['Content-Type'] = "image/png"
          self.response.headers['Cache-Control'] = "no-cache, must-revalidate"
          self.response.headers['Pragma'] = "no-cache"
          self.response.headers['Expires'] = "Sat, 26 Jul 1997 05:00:00 GMT"
          self.response.out.write(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=='))

app = webapp2.WSGIApplication([ ('/', MainHandler), 
                                ('/r/(.*)', RedirectHandler),
                                ('/worker', ExtractWorker),
                              ], debug=True)
