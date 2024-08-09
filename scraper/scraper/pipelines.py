import pymongo

from scraper import settings
from scrapy.exceptions import DropItem


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient("mongodb://localhost:27017/")
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
        return item