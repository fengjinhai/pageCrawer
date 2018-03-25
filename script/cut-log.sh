#! /bin/sh
#
# cut-log.sh
# Copyright (C) 2014 吴淋 <wulin03@baidu.com>
#
# Distributed under terms of the MIT license.
#


BASE_PATH=$(cd `dirname $0`;pwd)
LOG_PATH=$BASE_PATH/../log
YESTERDAY=$(date -d "yesterday" +%Y%m%d)
#cut every day
mv ${LOG_PATH}/dunews-selectsvr.log ${LOG_PATH}/dunews-selectsvr.log.${YESTERDAY}
