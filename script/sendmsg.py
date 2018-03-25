#-*- coding:utf-8 -*-
import socket
import sys,os,time

#emp01.baidu.com emp02.baidu.com emp03.baidu.com
basepath = os.path.split(os.path.realpath(__file__))[0]
warning_log = basepath + '/../log/monitor.log'
last_warning_time = 0
warnings = [v.strip() for v in open(warning_log) if v.strip()] 
if warnings:
    last_warning_time = int(warnings[-1].split(' ')[1].strip())
    delta = time.time() - last_warning_time
    if delta < 10*60:
        sys.exit(0)

fp = open(warning_log, 'a')
fp.write('warningsend %s' % int(time.time()))
fp.close()

phone_list = ['18701496016']
message = 'selectsvr warning alarm'
for phone in phone_list:
    g_smsserver="172.22.1.154"
    g_smsport=15001
    smsserver=(g_smsserver,g_smsport)
    gsmsend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
            gsmsend.connect(smsserver)
    except socket.error:
            sys.exit("cannt connect to server")
    gsmsend.send(("%s@%s" %(phone,message)).encode('gbk'))
    gsmsend.close()
