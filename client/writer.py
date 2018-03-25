'''
 * @file writer.py
 * @author zengwenjun(com@baidu.com)
 * @date 2014/10/09 20:06:01
 * @brief 
 *  
 '''

import threading
import time
import socket

class Writer:

    def __int__(self):
        pass

    def init(self, conf):
        self.conf = conf
        self.connlist = []
        for line in open(conf):
            data = line.strip().split(" ")
            if len(data) != 2:
                data = line.strip().split("\t")
            if len(data) != 2:
                continue
            self.connlist.append([data[0],int(data[1]),None,False]) #(ip,port,socket,used)
        self.cur_idx = 0
        self.m_nAvailableConCount = 0
        self.lock = threading.Lock()
        return self.initConnection()

    def initConnection(self):
        for conn in self.connlist:
            if not conn[2]:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    sock.connect((conn[0], conn[1]))
                    conn[2] = sock
                    conn[3] = False
                    self.m_nAvailableConCount += 1
                except:
                    print "connet to [%s:%d] fail" % (conn[0], conn[1])
                    sock.close()
        if self.m_nAvailableConCount > 0 :
            return True
        else:
            return False

    def Write(self, data):
        self.lock.acquire()
        if self.m_nAvailableConCount <= 0 :
            self.initConnection()
        if self.m_nAvailableConCount <= 0 :
            self.lock.release()
            print "FATAL : m_nAvailableConCount is 0"
            return False
        choose_conn = None
        while choose_conn is None:
            for i in range(0,len(self.connlist)):
                conn = self.connlist[self.cur_idx]
                self.cur_idx = (self.cur_idx+1)%len(self.connlist)
                if conn[2] and conn[3] == False:
                    choose_conn = conn
                    conn[3] = True
                    break
            if choose_conn is None:
                time.sleep(1)
        self.lock.release()
        try:
            choose_conn[2].sendall(data)
        except socket.error, e:
            choose_conn[2].close()
            choose_conn[2] = None
            self.lock.acquire()
            self.m_nAvailableConCount -= 1
            self.lock.release()
            choose_conn[3] = False
            print "WARNING WRITE ERROR[%d] : %s", (e.args[0], e.args[1])
            return False
        choose_conn[3] = False
        return True
