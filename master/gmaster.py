#coding: utf-8
import sys
import threading
import time
import signal
import task_queue 
import json

sys.path.append("../lib")
import http_server

class Master(object):
    def __init__(self, host, port):
        self.server = http_server.HttpServer(host, port)
        self.server.Register("/get_request", self.get_request)
        self.server.Register("/task_num", self.task_num)
        self.t = threading.Thread(target = self.read_tasks)
        self.read_seconds = 60
        self.stop_flag = threading.Event()
        self.tasks = task_queue.TaskQueue(3000000)
        self.task_reader = task_reader.TaskReader()

    def start(self):
        self.task_reader.clear_status()
        self.t.start()
        self.server.Start()

    def get_request(self, params):
        type_id = params.get("type", None)
        if not type_id:
            return "NULL"
        type_id = type_id[0]
        resp = self.tasks.get(type_id)
        print type_id,resp
        if resp != "NULL":
            self.task_reader.get_by_client(type_id, resp)
        return resp
 
    def read_tasks(self):
        task_num = 10000
        while True:
            print "read_tasks"
            self.task_reader.clear_timeout()
            while True:
                task_list = self.task_reader.read(task_num)
                put_status = 0
                success_tasks = []
                for task in task_list:
                    put_status = self.tasks.put(task)
                    if put_status == 1:
                        break
                    if put_status == 2:
                        continue
                    success_tasks.append(task)
                self.task_reader.get_by_master(success_tasks)

                #任务读完 or 队列满 or 程序结束
                if len(task_list) < task_num or put_status == 1 or self.stop_flag.is_set():
                    break
            if self.stop_flag.wait(timeout=self.read_seconds):
                break
        print "exit read_task"

    def task_num(self, params):
        return str(self.tasks.size())

    def shutdown(self, *args):
        self.server.ShutDown()
        print "start shutdown"
        self.stop_flag.set()

def main():
    global task_reader
    try:
        task_reader = __import__(sys.argv[2])
    except Exception, e:
        print e
        sys.exit(2)
    master = Master("", int(sys.argv[1]))
    t = threading.Thread(target = master.start)
    t.start()
    signal.signal(signal.SIGINT, master.shutdown)
    signal.signal(signal.SIGTERM, master.shutdown)
    signal.pause()
    t.join()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: %s <port> <task_reader>" % sys.argv[0]
        sys.exit(1)
    main()
