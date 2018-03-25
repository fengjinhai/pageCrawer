#coding: utf-8
import sys
import socket
host = '10.137.13.207'
port = 31415
forge = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
forge.connect((host, port))

def log(d):
    line = "||".join(["%s=%s" % (k,v) for k,v in d.iteritems()])
    try: forge.sendall(line)
    except Exception, e:
        print >> sys.stderr, e
