#coding: utf-8
import time
import re
import sys
import socket
import os
import threading
import httplib
import json
import dbwriter

sys.path.append("../lib")
import download
from log_conf import *
sys.path.append("..")
from conf import master_conf

master_host = master_conf.host
master_port = master_conf.port

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

class BaseClient:
    """
    @member
    task_type: client类型，子类必须赋值
    failed_time: 获取任务失败后sleep的秒数
    crawl_interval: 抓取间歇秒数
    """

    def __init__(self):
        self.task_type = None
        self.failed_time = 30
        self.crawl_interal = 1
        self.id = None
        self.ip = None

        #status_writer: 记录client抓取状态
        self.status_writer = dbwriter.ClientDBWriter()
        self.stop_flag = threading.Event()

    def get_request(self):
        try:
            conn = httplib.HTTPConnection(host=master_host, port=master_port, timeout=60)
            path = "/get_request?type=%s" % self.task_type
            conn.request("GET", path)
            response = conn.getresponse()
            resp = response.read()
            conn.close()
        except Exception, e:
            logging.error(e)
            return None
        if resp == "NULL":
            print "resp NULL"
            return None
        return resp

    def parse(self, page, url, type): return True

    def preprocess(self):
        if not self.task_type:
            logging.error("task_type is not defined!")
            return False
        ip = socket.gethostbyname(socket.gethostname())
        path = os.path.abspath("../")
        self.id = self.status_writer.register(ip, path, self.task_type, self.id)
        self.ip = ip
        if not self.id:
            logging.error("register client failed!")
            return False
        return True
 
    def start(self, id = None, task_type = None, is_proxy=0, retry=2):
        if not self.task_type:
            self.task_type = task_type
        self.id = id
        if not self.preprocess():
            return
        logging.info("%s client start!" % self.task_type)
        if is_proxy:
            getPage = download.getPageWithProxy
        else:
            getPage = download.getPage
        while True:
            if self.stop_flag.is_set():
                break
            #time.sleep(self.crawl_interal)
            resp = self.get_request()
            print 'resp:',resp
            logging.info(resp)
            self.status_writer.up_request_time()
            if not resp:
                logging.warning("get request failed")
                if self.stop_flag.wait(timeout=self.failed_time):
                    break
                continue
            item = json.loads(resp)
            url = item['url'].encode("utf-8", "ignore")
            ignore = False
            for p in exclude_url_pattern:
                if re.match(p, url):
                    ignore = True
                    print p, url
                    break
            if ignore: continue
            c = getPage(url, retry)
            if not c:
                self.status_writer.crawl_failed(url)
                continue
            ret = self.parse(c, url, item['type'])
            if not ret:
                self.status_writer.parse_failed(url)
                continue
            self.status_writer.success(url)
    
    def shutdown(self, *args):
        self.stop_flag.set()
        self.status_writer.shutdown()
