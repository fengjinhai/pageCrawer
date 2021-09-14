#! /bin/sh
#
# release.sh
# Copyright (C) 2015 冯锦海 <fengjinhai>
#
# Distributed under terms of the MIT license.
#


RELEASE_DIR=/home/work/dunews-release/dunews-selectsvr
WORK_DIR=/home/work/fengjinhai/dunews-selectsvr
HOST_DIR=/home/work/dunews-selectsvr
SOURCE_HOST=
HOSTS=

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
    ssh $host "cd ${HOST_DIR} && rm -rf bin.bak scripts.bak && cp bin bin.bak -R && cp scripts scripts.bak -R && tar xvf ${RELEASE_DIR}/$SOURCE_NAME && rm -rf ${RELEASE_DIR}/$SOURCE_NAME && cd scripts && sh restart.sh && exit"
done
