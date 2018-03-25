import sys
import csv
import hashlib
import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

sys.path.append("..")
from conf import mongo_conf

def main(name):
    client = MongoClient(mongo_conf.host, mongo_conf.port)
    db = client[mongo_conf.db]
    table = db['Sources']
    reader = csv.reader(open(name))
    i = 0
    for line in reader:
        i += 1
        if i == 1: continue
        md5 = hashlib.md5(line[3]).hexdigest()
        print md5
        doc = {'_id': ObjectId(md5[:24]),
                'DataSourceName': line[1],
                'WebSite': line[2],
                'Url': line[3],
                'Type': line[4],
                'CreateTime': datetime.datetime.now(),
                'CrawlTime': datetime.datetime.min,
                'CrawlNum': 0,
                'CrawlFailedNum': 0,
                'ParseFailedNum': 0,
                'StatusTime': datetime.datetime.now(),
                'Status': 0,
                'Freq': 600}
        try:
            table.insert(doc)
        except Exception, e:
            print e

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print 'Usage: %s <datasource.csv>' % sys.argv[0]
        sys.exit(1)
    main(sys.argv[1])
