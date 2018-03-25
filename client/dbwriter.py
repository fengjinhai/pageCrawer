#coding: utf-8
import sys
import os
import datetime
import hashlib
from pymongo import MongoClient
from bson.objectid import ObjectId

sys.path.append("../lib")
from log_conf import *
sys.path.append("..")
from conf import mongo_conf

class ClientDBWriter:
    def __init__(self):
        self.id = None
        self.task_type = None
        try:
            self.mongo = MongoClient(mongo_conf.host, mongo_conf.port)
            self.conn = self.mongo[mongo_conf.db]
        except Exception, e:
            logging.error("ClientDBWriter init error: %s" % e)
            self.conn = None

    def register(self, ip, path, task_type, id=None):
        self.task_type = task_type
        try:
            if not id:
                self.id = self.conn.ClientList.insert({
                    'Ip': ip, 'Path': path,
                    'TaskType': task_type, 'Pid': os.getpid(),
                    'CrawlNum': 0, 'CrawlFailedNum': 0,
                    'ParseFailedNum': 0})
                self.id = str(self.id)
            else:
                self.conn.ClientList.update({'_id': ObjectId(id)},
                        {'$set': {'Ip': ip, 'Path': path,
                            'TaskType': task_type, 'Pid': os.getpid()}},
                        multi = True)
                self.id = id
            return self.id
        except Exception, e:
            logging.error("db error: %s" % e)
            return None

    def up_request_time(self):
        self.conn.ClientList.update({'_id': ObjectId(self.id)},
                {'$set': {'RequestTime': datetime.datetime.now()}})
        
    def crawl_failed(self, url):
        _id = hashlib.md5(url).hexdigest()[:24]
        self.conn[self.task_type].update({'_id': ObjectId(_id)},
                {'$inc': {'CrawlNum': 1, 'CrawlFailedNum': 1},
                 '$set': {'CrawlTime': datetime.datetime.now()}})
        self.conn.ClientList.update({'_id': ObjectId(self.id)},
                {'$inc': {'CrawlNum': 1, 'CrawlFailedNum': 1},
                 '$set': {'CrawlTime': datetime.datetime.now()}})

    def parse_failed(self, url):
        _id = hashlib.md5(url).hexdigest()[:24]
        self.conn[self.task_type].update({'_id': ObjectId(_id)},
                {'$inc': {'CrawlNum': 1, 'ParseFailedNum': 1},
                 '$set': {'CrawlTime': datetime.datetime.now()}})
        self.conn.ClientList.update({'_id': ObjectId(self.id)},
                {'$inc': {'CrawlNum': 1, 'ParseFailedNum': 1},
                 '$set': {'CrawlTime': datetime.datetime.now()}})
               
    def success(self, url):
        _id = hashlib.md5(url).hexdigest()[:24]
        self.conn[self.task_type].update({'_id': ObjectId(_id)},
                {'$inc': {'CrawlNum': 1},
                 '$set': {'CrawlTime': datetime.datetime.now()}})
        self.conn.ClientList.update({'_id': ObjectId(self.id)},
                {'$inc': {'CrawlNum': 1},
                 '$set': {'CrawlTime': datetime.datetime.now()}})

    def shutdown(self):
        self.conn.ClientList.update({'_id': ObjectId(self.id)},
                {'$set': {'Pid': 0}})

    def __del__(self):
        if self.conn: self.mongo.close()
