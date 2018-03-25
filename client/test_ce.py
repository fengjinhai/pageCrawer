#coding=utf-8
import re
import sys
import time
import datetime
import base_client
import runner
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.binary import Binary
import dateutil.parser as dtparser
import hashlib
import zlib
from process import content_extract_new as ce

sys.path.append("../lib")
from log_conf import *
sys.path.append("..")
from conf import mongo_conf

class Client(base_client.BaseClient):
    def __init__(self):
        base_client.BaseClient.__init__(self)
        self.task_type = "Pages"
        try:
            self.mongo = MongoClient(mongo_conf.host, mongo_conf.port)
            self.conn = self.mongo[mongo_conf.db]
        except Exception, e:
            logging.error("Client init error: %s" % e)
        self.conn = None

    def start(self):
        url = ""
        page = open("process/page.html").read()
        type = ""
        self.parse(page, url, type)

    def parse(self, page, url, type):
        encoding, time, title, text, html, images = ce.parse(url, page)
        if not encoding:
            print "encoding None"
            return False
        
        _id = hashlib.md5(url).hexdigest()[:24]
        logging.info("%s\t%s" % (_id, url))
        return True

if __name__ == "__main__":
    runner.run(Client)
