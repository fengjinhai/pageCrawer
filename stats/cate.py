#encoding: utf-8
import csv
import hashlib
import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

cate = [   '综合新闻',
    '娱乐',
    '全球',
    '商业&财经',
    '科技',
    '生活',
    '健康&美容',
    '体育',
    '搞笑',
    '食物',
    '汽车',
    '旅行',
    '教育',
        ]

def main():
    client = MongoClient('mongodb://localhost:8317')
    db = client['dunews']
    table = db['Pages']
    for c in cate:
        print c, table.find({'Status':100, 'Type':c}).count()
    print 'ALL', table.find({'Status':100}).count()

if __name__ == "__main__":
    main()
