#!/usr/bin/env python
#coding=UTF-8
'''
    Created on 2013-11-20
    @author: devin
    @desc:
        http server
'''
import sys
import socket
import SocketServer
import SimpleHTTPServer
import urlparse


class ThreadedHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    dispatchers = {}
    
    @classmethod 
    def Register(self, path, fun):    
        self.dispatchers[path] = fun 

    def do_GET(self):
        o = urlparse.urlparse(self.path)
        params = urlparse.parse_qs(o.query)
        response = ''
        if o.path in self.dispatchers:
            fun = self.dispatchers[o.path]
            response = fun(params)
        #send data
        self.send_response(200)
        self.end_headers()
        self.wfile.write(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class HttpServer:
    def __init__(self, host, port):
        self.server = ThreadedTCPServer((host, port), ThreadedHTTPRequestHandler)

    def Register(self, path, fun):
        ThreadedHTTPRequestHandler.Register(path, fun)

    def Start(self):
        self.server.serve_forever()

    def ShutDown(self, *args):
        self.server.shutdown()

def Test(params):
    return "Test:" + str(params)

if __name__ == "__main__":
    HOST, PORT = "", 38000
    server = HttpServer(HOST, PORT)
    server.Register("/test", Test)
    server.Start()

