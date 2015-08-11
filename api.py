'''
Created on Aug 11, 2015
@author: yuanx
'''
import protorpc
import endpoints
from models import Category, Period, Dish
import main
from google.appengine.ext import ndb

@endpoints.api(name="aramarkHelperMenuFetcher", version="v1", description="Menu Fetcher API")
class MenuFetcherApi(protorpc.remote.Service):

    @Period.query_method(path="period/list/{selectDate}", name="period.list",
                         query_fields=("limit", "order", "pageToken", "selectDate"),
                         http_method="GET")
    def period_list(self, query):
        return query

    @Category.query_method(path="category/list/{parent}", name="category.list",
                           query_fields=("limit", "order", "pageToken", "parent"),
                           http_method="GET")
    def category_list(self, query):
        return query

    @Dish.query_method(path="dish/list/{parent}", name="dish.list",
                           query_fields=("limit", "order", "pageToken", "parent"),
                           http_method="GET")
    def dish_list(self, query):
        return query

app = endpoints.api_server([MenuFetcherApi], restricted=False)
