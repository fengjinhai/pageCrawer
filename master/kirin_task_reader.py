#coding: utf-8
import sys
import datetime
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
import util

sys.path.append("../lib")
from log_conf import *
sys.path.append("..")
from conf import mongo_conf

class TaskReader(object):
    def __init__(self):
        try:
            self.client = MongoClient(mongo_conf.host, mongo_conf.port)
            self.conn = self.client[mongo_conf.db]
        except Exception, e:
            logging.error("TaskReader init error: %s" % e)
            self.conn = None

    def __del__(self):
        if self.conn: self.client.close()
    
    def read(self, limit):
        if not self.conn: return []
        
        now = datetime.datetime.now()
        t = int(now.strftime("%s"))
        criteria = '%d-this.CrawlTime.getTime()/1000+8*3600>=this.Freq && this.Status == 0' % t
        logging.info("read tasks: %s" % criteria)
        result = self.conn.Sources.find({'$where': criteria}).limit(limit)
        ret = []
        for res in result:
            url = res['Url'].encode("utf-8")
            news_type = res['Type'].encode("utf-8")
            item = {'url':url, 'type': news_type}
            task_type = 'Sources'
            try: priority = int(res['CrawlTime'].strftime("%s"))
            except: priority = 0
            ret.append((priority, task_type, json.dumps(item)))
        sources_num = len(ret)

        # 详情页task
        logging.info("load Pages tasks")
        result = self.conn.Pages.find({'Status': 0}).limit(limit)
        for res in result:
            url = res['Url'].encode("utf-8")
            news_type = res['Type'].encode("utf-8")
            item = {'url': url, 'type': news_type}
            task_type = "Pages"
            priority = int(res['DiscoverTime'].strftime("%s"))
            ret.append((priority, task_type, json.dumps(item)))
        total = len(ret)
        logging.info("%d tasks: %d sources, %d pages" % (total, sources_num, total-sources_num))
        return ret

    def get_by_master(self, tasks):
        if not tasks: return 0
        if not self.conn: return 0
        ret = 0
        for priority, task_type, resp in tasks:
            item = json.loads(resp)
            url = item['url'].encode("utf-8", "ignore")
            _id = util.md5(url)[:24]
            try:
                self.conn[task_type].update({'_id': ObjectId(_id)},
                        {'$set': {'Status': 1, 'StatusTime': datetime.datetime.now()}},
                        multi = True)
                ret += 1
            except:
                continue
        return ret

    def get_by_client(self, task_type, resp):
        if not self.conn: return 0
        if not resp: return 0
        item = json.loads(resp)
        url = item['url'].encode("utf-8", "ignore")
        _id = util.md5(url)[:24]        
        try:
            self.conn[task_type].update({'_id': ObjectId(_id)},
                    {'$set': {'Status': 2, 'StatusTime': datetime.datetime.now()}},
                    multi = True)
        except Exception, e:
            print 'error:', type(url), _id
        ret = 1
        return ret

    def clear_status(self):
        if not self.conn: return 0
        for c in ['Sources', 'Pages']:
            self.conn[c].update({'Status': 1},
                {'$set': {'Status': 0, 'StatusTime': datetime.datetime.now()}},
                multi = True)
        ret = 1
        return ret

    def clear_timeout(self):
        if not self.conn: return 0

        # 清除抓取5次不成功的
        now = datetime.datetime.now()
        t = int(now.strftime("%s"))
        for doc in self.conn.Pages.find({'Status':2},{'CrawlFailedNum':1}):
            if doc['CrawlFailedNum'] >= 5:
                self.conn.Pages.update({'_id': doc['_id']},
                    {'$set': {'Status': 101, 'StatusTime': now}},
                    multi = True)

        # 抓取不成功的重置为待抓取，距离抓取5分钟
        now = datetime.datetime.now()
        t = int(now.strftime("%s"))
        for c in ['Sources', 'Pages']:
            for doc in self.conn[c].find({'Status':2},{'StatusTime':1}):
                if int(doc['StatusTime'].strftime("%s")) < t-300:
                    self.conn[c].update({'_id': doc['_id']},
                        {'$set': {'Status': 0, 'StatusTime': now}},
                        multi = True)
        ret = 1
        return ret
    
