#! /bin/sh
#
# release.sh
# Copyright (C) 2015 吴淋 <wulin03@baidu.com>
#
# Distributed under terms of the MIT license.
#


RELEASE_DIR=/home/work/dunews-release/dunews-selectsvr
WORK_DIR=/home/work/dunews/dunews-selectsvr
SOURCE_HOST=cq01-globalpm-eval1-5.cq01.baidu.com
HOSTS="work@nj02-gnews-app00.nj02"
#HOSTS="work@nj02-gnews-app00.nj02"
SOURCE_NAME=dunews-selectsvr.tar
[[ -d ${RELEASE_DIR} ]] || mkdir -p ${RELEASE_DIR}
cd ${RELEASE_DIR}
rm -rf bin scripts
cp ${WORK_DIR}/bin . -R
cp ${WORK_DIR}/scripts . -R
find bin -type d -name '.svn' | xargs rm -rf
find bin -type f -name '.pyc' | xargs rm -rf
find scripts -type d -name '.svn' | xargs rm -rf
find scripts -type f -name '.pyc' | xargs rm -rf
tar cvf $SOURCE_NAME bin scripts
rm -rf bin scripts
for host in $HOSTS
do
    ssh $host "[[ -d ${RELEASE_DIR} ]] || mkdir -p ${RELEASE_DIR}"
    scp $SOURCE_NAME $host:$RELEASE_DIR
    ssh $host "cd ${WORK_DIR} && rm -rf bin.bak scripts.bak && cp bin bin.bak -R && cp scripts scripts.bak -R && tar xvf ${RELEASE_DIR}/$SOURCE_NAME && rm -rf ${RELEASE_DIR}/$SOURCE_NAME && cd scripts && source ~/.bash_profile && sh restart.sh && exit"
done
