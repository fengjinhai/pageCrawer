#coding=utf-8
import nshead
import mcpack
import writer
import time
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
        self.catg = {u'综合新闻':6, u'娱乐':3, u'全球':1 ,u'商业&财经':5, u'科技':4, u'生活':14, u'健康&美容':14, u'体育':2, u'搞笑':11, u'食物':12, u'汽车':8, u'旅行':13, u'教育':9}
        base_client.BaseClient.__init__(self)
        self.task_type = "Pages"
        self.writer = writer.Writer()
        self.writer.init('../conf/selectsvr.conf')
        try:
            self.mongo = MongoClient(mongo_conf.host, mongo_conf.port)
            self.conn = self.mongo[mongo_conf.db]
        except Exception, e:
            logging.error("Client init error: %s" % e)
            self.conn = None

    def selectsvr_send(self, sendpack):
        head = nshead.NsHead()
        #mcpack_body = mcpack.dumps(packData, charset='gb18030')
        mcpack_body = mcpack.dumps(sendpack)
        head.body_len = len(mcpack_body)
        request = head.pack() + mcpack_body
        if not self.writer.Write(request):
            print " get cluster writer fail lang %d type %d url %s" % (sendpack['language'], sendpack['type'], sendpack['url'])
            return False
        return True


    def parse(self, page, url, type):
        encoding, publish_time, title, text, html, images = ce.parse(url, page)
        if not encoding:
            print "encoding None"
            return False
        
        if title == '':
            print "title None"
            return False


        dr = re.compile(r'<[^>]+>',re.S)
        title = dr.sub('',title)

        _id = hashlib.md5(url).hexdigest()[:24]
        logging.info("%s\t%s" % (_id, url))
        
        publish_time_stamp = 0
        try:
            publish_time_stamp = time.mktime(dtparser.parse(publish_time).timetuple())
        except Exception, e:
            logging.info(e)

        self.conn.Pages.update({'_id': ObjectId(_id)}, {'$set':
                {
                #'ZipHtml': Binary(zlib.compress(page)),
                 'Encoding': encoding,
                 'Title': title,
                 'Content': text,
                 'Html': html,
                 'Images': images,
                 'CrawlTime': datetime.datetime.now(),
                 'StatusTime': datetime.datetime.now(),
                 'PubTime': dtparser.parse(publish_time),
                 'Status': 100}})

        packDic = {
                "pub-time-stamp": int(time.time()),
                "update_time": int(time.time()),
                "real-title": title,
                "language": 0,
                "McPackSrc": 'CS',
                "pagecrawl_time": int(time.time()),
                #"MAIN_PIC": images,
                "main-pic": images,
                "url":url,
                "url_md5": hashlib.md5(url).hexdigest(),
                "mask_key":abs(hash(url)),
                "html": html,
                #"content": html,
                "real-title": title,
                "type": 1,
                "classify": self.catg[type], 
                "pub-time": publish_time_stamp #time.mktime(dtparser.parse(publish_time).timetuple())
        }
        print packDic
        self.selectsvr_send(packDic)
        return True

if __name__ == "__main__":
    runner.run(Client)
