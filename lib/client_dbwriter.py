#coding: utf-8
import MySQLdb
import logging
import logging.handlers
import json
import sys
import time
import util
import os
from mysql_conf import *

class ClientDBWriter:
    def __init__(self):
        self.db_connect()
        self.logger = logging.getLogger("client_log")
        self.id = None
        self.task_type = None

    def register(self, ip, path, task_type, id=None):
        self.task_type = task_type
        try:
            cursor = self.db_conn.cursor()
            if not id:
                sql = "INSERT INTO client_list(ip, path, task_type, pid) "\
                        "VALUES('%s', '%s', '%s', %d)" \
                        % (ip, path, task_type, os.getpid())
                cursor.execute(sql)
                self.id = self.db_conn.insert_id()
            else:
                sql = "UPDATE client_list SET ip='%s', path='%s', task_type='%s', pid=%d "\
                        "WHERE id=%d" % (ip, path, task_type, os.getpid(), id)
                cursor.execute(sql)
                self.id = id
            self.db_conn.commit()
            return self.id
        except Exception, e:
            print >>sys.stderr, "db error: %s" % e #这时候self.logger还没有注册handler
            return None

    def up_request_time(self):
        sql = "UPDATE client_list SET request_time=now() WHERE id=%d" % self.id
        self.db_operator(sql)

    def shutdown(self):
        sql = "UPDATE client_list SET pid=0 WHERE id=%d" % self.id
        self.db_operator(sql)

    def crawl_failed(self, url, batch_id):
        self.logger.error("crawl %s failed" % url)
        crawl_time = time.time()
        sql_url = "UPDATE list_url SET crawl_time=FROM_UNIXTIME(%d), crawl_status=1, status=3, status_time=now() " \
                "WHERE url_md5='%s' AND batch_id=%d AND UNIX_TIMESTAMP(crawl_time) <= %d" % \
                (crawl_time, util.md5(url), batch_id, crawl_time)
        sql_client = "UPDATE client_list SET crawl_time=FROM_UNIXTIME(%d), crawl_num=crawl_num+1, " \
                "crawl_failed_num=crawl_failed_num+1 WHERE id=%d" % (crawl_time, self.id)
        sql_task_batch = "UPDATE task_batch SET last_crawl_time=FROM_UNIXTIME(%d), crawl_num=crawl_num+1, "\
                "crawl_failed_num=crawl_failed_num+1 "\
                "WHERE task_type='%s' and batch_id=%d" % (crawl_time, self.task_type, batch_id)
        self.db_operator(sql_url)
        self.db_operator(sql_client)
        self.db_operator(sql_task_batch)

    def parse_failed(self, url, batch_id):
        self.logger.error("parse %s failed" % url)
        crawl_time = time.time()
        sql_url = "UPDATE list_url SET crawl_time=FROM_UNIXTIME(%d), crawl_status=2, status=3, status_time=now() " \
                "WHERE url_md5='%s' AND batch_id=%d, UNIX_TIMESTAMP(crawl_time) <= %d" % \
                (crawl_time, util.md5(url), batch_id, crawl_time)
        sql_client = "UPDATE client_list SET crawl_time=FROM_UNIXTIME(%d), crawl_num=crawl_num+1, " \
                "parse_failed_num=parse_failed_num+1 WHERE id=%d" % (crawl_time, self.id)
        sql_task_batch = "UPDATE task_batch SET last_crawl_time=FROM_UNIXTIME(%d), crawl_num=crawl_num+1, "\
                "parse_failed_num=parse_failed_num+1 "\
                "WHERE task_type='%s' and batch_id=%d" % (crawl_time, self.task_type, batch_id)
        self.db_operator(sql_url)
        self.db_operator(sql_client)
        self.db_operator(sql_task_batch)

    def succeed(self, url, detail_urls, batch_id):
        crawl_time = time.time()
        self.logger.info("parse %s successful" % url)
        sql_url = "UPDATE list_url SET crawl_time=FROM_UNIXTIME(%d), crawl_status=0, status=3, status_time=now() " \
                "WHERE url_md5='%s' AND batch_id=%d AND UNIX_TIMESTAMP(crawl_time) <= %d" % \
                (crawl_time, util.md5(url), batch_id, crawl_time)
        sql_client = "UPDATE client_list SET crawl_time=FROM_UNIXTIME(%d), crawl_num=crawl_num+1 "\
                "WHERE id=%d" % (crawl_time, self.id)
        sql_task_batch = "UPDATE task_batch SET last_crawl_time=FROM_UNIXTIME(%d), crawl_num=crawl_num+1, "\
                "parse_url_num=parse_url_num+%d WHERE task_type='%s' and batch_id=%d" % \
                (crawl_time, len(detail_urls), self.task_type, batch_id)
        self.db_operator(sql_url)
        self.db_operator(sql_client)
        self.db_operator(sql_task_batch)
        table_name = "detail_urls_%s" % time.strftime("%Y%m%d", time.localtime(crawl_time))
        sql_create = """CREATE table IF NOT EXISTS %s (
        `id` int(11) NOT NULL auto_increment,
        `url` text NOT NULL,
        `list_url` text NOT NULL,
        `task_type` varchar(20) NOT NULL,
        `client_id` int(11) NOT NULL,
        `batch_id` int(11) NOT NULL default 1,
        `update_time` timestamp NOT NULL default CURRENT_TIMESTAMP,
        PRIMARY KEY  (`id`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8""" % table_name
        self.db_operator(sql_create)
        sql_insert = "INSERT INTO %s(url, list_url, task_type, client_id, batch_id) VALUES" % table_name;
        values = ",".join(["('%s', '%s', '%s', %d, %d)" % \
                (detail_url, url, self.task_type, self.id, batch_id) for detail_url in detail_urls])
        sql_insert +=values
        self.db_operator(sql_insert)

    def get_cur_batch(self):
        self.db_connect()
        if not self.db_conn:
            return None
        try:
            cursor = self.db_conn.cursor()
            sql = "SELECT max(batch_id) FROM task_batch WHERE task_type='%s'" % self.task_type
            ret = cursor.execute(sql)
            if not ret:
                self.db_conn.commit()
                return None
            batch_id = cursor.fetchone()[0]
            self.db_conn.commit()
            return batch_id
        except:
            return None

    def reset_error(self):
        batch_id = self.get_cur_batch()
        if not batch_id:
            return
        sql_url = "UPDATE list_url SET status=0, status_time=now() WHERE task_type='%s' AND "\
                "batch_id=%d AND status=3 AND crawl_status!=0" % (self.task_type, batch_id)
        self.db_operator(sql_url)

    def db_connect(self):
        try:
            self.db_conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, charset="utf8")
        except:
            self.logger.error("db connect failed")
            self.db_conn = None

    def db_ping(self):
        try:
            self.db_conn.ping()
        except:
            self.db_connect()

    def db_operator(self, sql):
        self.db_ping()
        exe_ret = None
        if not self.db_conn:
            return None
        try:
            cursor = self.db_conn.cursor()
            exe_ret = cursor.execute(sql)
            self.db_conn.commit()
        except Exception, e:
            self.logger.error("%s %s, db Error" % (sql, e))
        return exe_ret

    def __del__(self):
        if self.db_conn:
            self.db_conn.close()
