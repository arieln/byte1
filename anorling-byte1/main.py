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

import feedparser

import logging

import urllib

# this is for displaying HTML
from webapp2_extras import jinja2

# BaseHandler subclasses RequestHandler so that we can use jinja
class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

        # This will call self.response.write using the specified template and context.
        # The first argument should be a string naming the template file to be used. 
        # The second argument should be a pointer to an array of context variables
        #  that can be used for substitutions within the template
    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)

# Class MainHandler now subclasses BaseHandler instead of webapp2
class MainHandler(BaseHandler):
         # This method should return the html to be displayed
    def get(self):

        #Yahoo pipes url with default search for black
        feed = feedparser.parse("http://pipes.yahoo.com/pipes/pipe.run?_id=e05ccc83309131297c2e815b4b93d86e&_render=rss&filterbycolor=black")
        
        # dictionaries for RSS feed 
        feed = [{"link" : item.link, "title" : item.title, "description" : item.description} for item in feed["items"]]

        # feed context and default search term
        context = {"feed" : feed, "search" : "black"}

                  # here we call render_response instead of self.response.write.
        self.render_response('index.html', **context)

    def post(self):

        # this retrieves the contents of the search term 
        terms = self.request.get('search_term')
        quoted_terms = urllib.quote(terms)


        # terms provided by the user in the form
        feed = feedparser.parse("http://pipes.yahoo.com/pipes/pipe.run?_id=e05ccc83309131297c2e815b4b93d86e&_render=rss&filterbycolor=" + terms )
        
        # this sets up feed as a list of dictionaries containing information 
        feed = [{"link": item.link, "title":item.title, "description" : item.description} for item in feed["items"]]

        # this sets up the context with the user's search terms and the search
        # results in feed
        context = {"feed": feed, "search": terms}

        # this sends the context and the file to render to jinja2
        self.render_response('index.html', **context)

app = webapp2.WSGIApplication([('/.*', MainHandler)], debug=True)

