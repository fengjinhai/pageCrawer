#coding:utf-8
import re
from dateutil.parser import parse
RE_DATETIME = ur'(((\d{4}年){0,1}\d{1,2}月\d{1,2}日|(\d{4}-){0,1}\d{1,2}-\d{1,2})\s*?(\d{1,2}:\d{1,2}(:\d{1,2}){0,1}){0,1})'
RE_DATETIME = ur'(((\d{4}年){0,1}\d{1,2}月\d{1,2}日|(\d{4}-){0,1}\d{1,2}-\d{1,2})\s*(\d{1,2}:\d{1,2}(:\d{1,2}){0,1}){0,1})'
RE_DT_REPLACE = ur'年|月'
line = u'吴海宏07月01日 17:05 分享到： Google Android 分类 : 互联网吴海宏06月01日 17:05 分享到： Google Android 分类 : 互联网'
line = u'2014年07月01日16:28'
line = u'2014年07月01日22:21'

'''
for i in re.findall(RE_DATETIME, line):
    t = re.sub(RE_DT_REPLACE,'-',i[0]).replace(u'日',' ')
    print parse(t,fuzzy=True)

RE_IMG = ur'(?is)(<img.*?>)'
html = open('img.html').read()
import html_util
import hashlib
ec, html = html_util.get_unicode_str(html)
for i in re.findall(RE_IMG, html):
    md5 = hashlib.md5(i.encode('utf-8','ignore')).hexdigest()
    html = html.replace(i, md5)
print html.encode('utf-8')
'''
text = open('/tmp/raw.txt').read().decode('utf-8')
print re.findall(RE_DATETIME, text)
