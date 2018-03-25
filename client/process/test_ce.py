#encoding: utf-8
import sys
import content_extract as ce
sys.path.append("../../lib")
import download

if __name__ == "__main__":
    html = download.getPage(sys.argv[1])
    enc, time, title, text = ce.parse(sys.argv[1],html)
    print "标题："+title.encode('utf-8','ignore')
    print "时间："+time.encode('utf-8','ignore')
    print '='*10
    print "内容："+text.encode('utf-8','ignore')

