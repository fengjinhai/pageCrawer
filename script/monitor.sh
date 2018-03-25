#!/bin/bash
#===============================================================================
#
#          FILE:  monitor.sh
# 
#         USAGE:  ./monitor.sh 
# 
#   DESCRIPTION:  
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:   (), 
#       COMPANY:  Baidu.com, Inc
#       VERSION:  1.0
#       CREATED:  01/27/2015 04:32:12 PM CST
#      REVISION:  ---
#===============================================================================

source ~/.bash_profile
basepath=$(cd `dirname $0`;pwd)
last_insert_time=`tail -1000 ${basepath}/../log/dunews-selectsvr.log | grep 'insert ok' | tail -1 | awk '{print $1,$2}'`
last_insert_timestamp=`date -d "$last_insert_time" +%s`
now=`date +%s`
let delta=now-last_insert_timestamp
if [ "$delta" -gt "300" ];then
    echo 'warning'
    python ${basepath}/sendmsg.py
else
    echo 'normal'
fi
