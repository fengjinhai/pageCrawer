#coding: utf-8
import Queue
import threading

class TaskQueue(object):
    def __init__(self, q_size):
        self.queue_dict = {}
        self.q_size = 0
        self.cur_size = 0
        if q_size > self.q_size:
            self.q_size = q_size
        self.task_set = set()
        self.set_lock = threading.Lock()
        self.dict_lock = threading.Lock()

    def get(self, type_id):
        self.dict_lock.acquire()
        p_q = self.queue_dict.get(type_id, None)
        self.dict_lock.release()

        if not p_q:
            return "NULL"
        task = "NULL"
        try:
            item = p_q.get_nowait()
            p_q.task_done()
            task = item[1]
        except:
            return "NULL"
        self.set_lock.acquire()
        self.task_set.discard((type_id, task))
        print len(self.task_set) 
        self.cur_size -= 1
        self.set_lock.release()
        return task

    def put(self, task):
        """
        加入任务，只允许单线程加入
        @return: 0 成功加入; 1 队列满; 2插入异常
        """

        priority = task[0]
        task_type = task[1]
        task_content = task[2]

        self.dict_lock.acquire()
        if task_type not in self.queue_dict:
            self.queue_dict[task_type] = Queue.PriorityQueue()
        self.dict_lock.release()

        self.set_lock.acquire()
        if (task_type, task_content) in self.task_set: #任务已存在
            self.set_lock.release()
            return 0
        if self.cur_size >= self.q_size: #队列满
            self.set_lock.release()
            return 1
        self.set_lock.release()
        
        self.dict_lock.acquire()
        p_q = self.queue_dict[task_type]
        self.dict_lock.release()
        
        try:
            p_q.put_nowait((priority, task_content))
        except:
            return 2 #优先队列异常
        self.set_lock.acquire()
        self.task_set.add((task_type, task_content))
        self.cur_size += 1
        self.set_lock.release()
        return 0 #任务顺利加入队列

    def size(self):
        self.set_lock.acquire()
        ret = self.cur_size
        self.set_lock.release()
        return ret

