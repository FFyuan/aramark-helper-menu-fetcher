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
import urllib2
import urllib
import os
from bs4 import BeautifulSoup
from models import Category, Dish, Period
from google.appengine.ext import ndb
import jinja2

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/menufetcher.html")
        self.response.out.write(template.render())

    def post(self):
        MainHandler.putMenu(self, self.request.get('date'), 481)
        MainHandler.putMenu(self, self.request.get('date'), 482)
        MainHandler.putMenu(self, self.request.get('date'), 483)
        MainHandler.putMenu(self, self.request.get('date'), 1778)
        MainHandler.putMenu(self, self.request.get('date'), 1779)

    def putMenu(self, date, periodId):
        """ date format: XXXX-XX-XX, peroid: 481,482,483 for breakfast, lunch and dinner, 1778 and 1779 for other two """
        values = {}
        values['LocationId'] = "1965"  # fixed for ARA
        values['PeriodId'] = periodId  # 481,482,483 for breakfast, lunch and dinner, 1778 and 1779 for other two
        values['MenuDate'] = date
        values['UIBuildDateForm'] = date
        data = urllib.urlencode(values)
        url = "http://rose-hulman.campusdish.com/Commerce/Catalog/Menus.aspx"
        geturl = url + "?" + data
        print geturl
        request = urllib2.Request(geturl)
        response = urllib2.urlopen(request)
        soup = BeautifulSoup(response.read())
        blocks = soup.find_all('div', class_='menu-details-station')

        if periodId == 481:
            pName = "Breakfast"
        elif periodId == 482:
            pName = "Lunch"
        elif periodId == 483:
            pName = "Dinner"
        elif periodId == 1778:
            pName = "Con't Breakfast"
        elif periodId == 1779:
            pName = "Soup & Salad"

        period = Period(selectDate=date,
                        name=pName)
        period.put()
        for block in blocks:
            # print block.h2.string, "------"
            category = Category(parent=period.entityKey,
                                name=block.h2.string)
            category.put()
            for item in block.find_all('div', class_='menu-name'):
                # print "     ", item.a.string
                dish = Dish(parent=category.entityKey,
                            name=item.a.string)
                dish.put()
        # self.response.write("Finish finding the period")
        # end of putMenu
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
