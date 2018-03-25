#! /bin/sh
#
# restart.sh
# Copyright (C) 2014 吴淋 <wulin03@baidu.com>
#
# Distributed under terms of the MIT license.
#

pid=$(ps aux | grep python | grep dunews-selectsvr.py | grep python | awk '{print $2}' | head -1)
if [[ ! -z "$pid" ]] && [[ $pid -gt 0 ]];then
    kill -9 $pid
fi
sleep 2
mp=`dirname $0`
cd $mp/../
nohup python bin/dunews-selectsvr.py &
