#coding: utf-8
import MySQLdb
import sys
from mysql_conf import *
import util

class TaskReader(object):
    def connect(self):
        try:
            conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, charset="utf8")
            return conn
        except:
            return None
    
    def read(self, limit):
        conn = self.connect()
        if not conn:
            return []
        
        sql = "SELECT url, task_type, batch_id, UNIX_TIMESTAMP(add_time) FROM list_url WHERE status=0" \
                " LIMIT %d" % limit
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
        except:
            return []
        ret = []
        for res in cursor.fetchall():
            url = res[0].encode("utf-8")
            task_type = res[1].encode("utf-8")
            batch_id = res[2]
            priority = res[3]
            ret.append((priority, task_type, "%d %s" % (batch_id, url)))
        cursor.close()
        conn.close()
        return ret

    def get_by_master(self, tasks):
        if not tasks:
            return 0
        conn = self.connect()
        if not conn:
            return 0
        ret = 0
        cursor = conn.cursor()
        for priority, task_type, task_content in tasks:
            batch_id, url = self.parse_task(task_content)
            try:
                sql = "UPDATE list_url SET status=1, status_time=now() "\
                        "WHERE url_md5='%s' AND task_type='%s' AND batch_id=%d AND status=0" \
                        % (util.md5(url),task_type, batch_id)
                ret += cursor.execute(sql)
            except:
                continue
        cursor.close()
        conn.commit()
        conn.close()
        return ret

    def get_by_client(self, task_type, batch_id_url):
        conn = self.connect()
        if not conn:
            return 0
        batch_id, url = self.parse_task(batch_id_url)
        if not url:
            return 0
        sql = "UPDATE list_url SET status=2, status_time=now() "\
                "WHERE url_md5='%s' AND task_type='%s' AND batch_id=%d" \
                % (util.md5(url), task_type, batch_id)
        cursor = conn.cursor()
        ret = cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()
        return ret

    def clear_status(self):
        conn = self.connect()
        if not conn:
            return 0
        sql = "UPDATE list_url SET status=0, status_time=now() WHERE status=1"
        cursor = conn.cursor()
        ret = cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()
        return ret

    def clear_timeout(self):
        conn = self.connect()
        if not conn:
            return 0
        sql = "UPDATE list_url SET status=0, status_time=now() WHERE status=2 "\
                "AND UNIX_TIMESTAMP(status_time) < UNIX_TIMESTAMP() - 1800"
        cursor = conn.cursor()
        ret = cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()
        return ret
    
    @staticmethod
    def parse_task(task):
        if not task:
            return (None, None)
        pos = task.find(' ')
        if pos < 0:
            return (None, None)
        try:
            batch_id = int(task[:pos])
            url = task[pos+1:]
            return (batch_id, url)
        except:
            return (None, None)
