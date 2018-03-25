#encoding=utf-8
import sys
import re
import datetime
import base_client
import runner
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.binary import Binary
import hashlib
import zlib
from process import list_extract as le

sys.path.append("../lib")
from log_conf import *
sys.path.append("..")
from conf import mongo_conf

exclude_url_pattern = [
        r".*\?ts=frontpagerecentlyviewed$",
        r".*\.pdf$",
        r".*readpdf.*",
        r"http://www.youtube.com/.*",
        r"http://.*\.squawka\.com/.*matches$",
        r"http://www.catchnews.com/.*\.html#answer.*",
        r"http://www.greaterkashmir\.com.*",
        r"http://www.freepressjournal\.in.*",
        r"http://telecomtalk\.info.*",
        r"http://.*#replies$",
        ]

class Client(base_client.BaseClient):
    def __init__(self):
        base_client.BaseClient.__init__(self)
        self.task_type = "Sources"
        try:
            self.mongo = MongoClient(mongo_conf.host, mongo_conf.port)
            self.conn = self.mongo[mongo_conf.db]
        except Exception, e:
            logging.error("Client init error: %s" % e)
            self.conn = None

    def parse(self, page, url, type):
        encoding, links = le.parse(url, page)
        if not encoding: return False
        for anchor, link in links:
            ok = True
            for p in exclude_url_pattern:
                if re.match(p, link):
                    ok = False
                    break
            if ok:
                self.add_endpage_link(link, url, type)

        '''
        doc = {'SourceUrl': url,
                'Type': type,
                'ZipHtml': Binary(zlib.compress(page)),
                'Encoding': encoding,
                'RunTime': datetime.datetime.now(),
                'LinkNum': len(links)}
        self.conn.EntryPages.insert(doc)
        '''
        return True

    def add_endpage_link(self, link, url, type):
        if isinstance(link, unicode): link = link.encode('utf-8', 'ignore')
        if isinstance(url, unicode): url = url.encode('utf-8', 'ignore')
        _id = hashlib.md5(link).hexdigest()[:24]
        endpage = self.conn.Pages.find({'_id': ObjectId(_id)},{'_id': 1}).count()
        if endpage > 0: return True
        doc = {'_id': ObjectId(_id), 'Url': link, 'SourceUrl': url, 'Type': type,
               'DiscoverTime': datetime.datetime.now(),
               'StatusTime': datetime.datetime.now(), 'Status': 0,
               'CrawlNum': 0, 'CrawlFailedNum': 0, 'ParseFailedNum': 0}
        try:
            self.conn.Pages.insert(doc)
        except Exception, e:
            logging.error(e)

if __name__ == "__main__":
    runner.run(Client)
