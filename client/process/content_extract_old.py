#coding=utf-8
import re
import hashlib
import dateutil.parser as dtparser
import lxml
import lxml.html
import lxml.etree
import html_util

RE_MULTI_NEWLINE = ur'\n+'

RE_IGNORE_BLOCK = {
'doctype' : ur'(?is)<!DOCTYPE.*?>', # html doctype
'comment' : ur'(?is)<!--.*?-->', # html comment
'script' : ur'(?is)<script.*?>.*?</script>', # javascript
'style' : ur'(?is)<style.*?>.*?</style>', # css
#'special' : ur'&.{2,5};|&#.{2,5};',
}

RE_NEWLINE_BLOCK = {
'div' : ur'(?is)<div.*?>',
'p' : ur'(?is)<p.*?>',
'br' : ur'(?is)<br.*?>',
'hr' : ur'(?is)<hr.*?>',
'h' : ur'(?is)<h\d+.*?>',
'li' : ur'(?is)<li\d+.*?>',
}

RE_IMG = ur'(?is)(<img.*?>)'

RE_IMG_SRC = ur'(?is)<img.+?src=(\'|")(.+?)(\'|").*?>'

RE_TAG = ur'(?is)<.*?>'

RE_TITLE = ur'(?is)<title.*?>(.+?)</title>'
RE_H = ur'(?is)<h\d+.*?>(.*?)</h\d+>'

RE_DATETIME = ur'(((\d{4}年){0,1}\d{1,2}月\d{1,2}日|(\d{4}-){0,1}\d{1,2}-\d{1,2})\s*(\d{1,2}:\d{1,2}(:\d{1,2}){0,1}){0,1})'

## parameters
BLOCKS_WIDTH = 3
THRESHOLD = 100

## 导航条特征
NAV_SPLITERS = [
    ur'\|',
    ur'┊',
    ur'-',
    ur'\s+',
]

def strtotime(t):
    if t == '': return ''
    RE_DT_REPLACE = ur'年|月'
    t = re.sub(RE_DT_REPLACE,'-',t).replace(u'日',' ')
    try:
        s = str(dtparser.parse(t, fuzzy=True))
    except:
        s = ''
    return s

def is_useful_line(line):
    for sep in NAV_SPLITERS:
        items = re.split(sep, line)
        if len(items) >= 5:
            return False
    return True

def get_raw_info(html):
    if not isinstance(html, unicode):
        return '','',''
    title = ''.join(re.findall(RE_TITLE, html))# + re.findall(RE_H, html)
    html = re.sub(ur"(?is)</a><a",'</a> <a',html)
    h = re.findall(RE_H, html)
    for ht in h:
        ht = ht.strip()
        if ht == '': continue
        if title.startswith(ht):
            title = ht
            break
    for k,v in RE_IGNORE_BLOCK.iteritems():
        html = re.sub(v, '', html)
    for k,v in RE_NEWLINE_BLOCK.iteritems():
        html = re.sub(v, '\n', html)
    html = re.sub(RE_MULTI_NEWLINE, '\n', html)
    
    return html_util.unescape(title), html_util.unescape(html)

def get_main_content(html):
    if not isinstance(html, unicode):
        return '',''

    html_lines_len = [len(x.strip()) for x in html.split('\n')]

    # 保存图片信息
    images = {}
    for img in re.findall(RE_IMG, html):
        md5 = hashlib.md5(img.encode('utf-8','ignore')).hexdigest()[:16]
        html = html.replace(img, md5)
        r = re.findall(RE_IMG_SRC, img)
        if len(r) == 1: src = r[0][1]
        else: src = ''
        images[md5] = "<img src='%s'>" % src#img

    # 去除所有的html标签
    text = re.sub(RE_TAG, '', html)

    # 抽取发表时间
    time = ''
    t = re.findall(RE_DATETIME, text)
    if len(t) > 0:
        time = t[0][0]

    lines = [x.strip() if is_useful_line(x) else '' for x in text.split('\n')]
    index_dist = []
    size = len(lines)
    for i in xrange(size - BLOCKS_WIDTH + 1):
        char_num = 0
        for j in xrange(i, i + BLOCKS_WIDTH):
            strip = re.sub(ur'\s+', '', lines[j])
            char_num += len(strip)
        index_dist.append(char_num)
    main_text = ''
    fstart = -1
    start = -1
    end = -1
    flag_s = False
    flag_e = False
    first_match = True
    for i in xrange(len(index_dist) - 1):
        if first_match and not flag_s:
            if index_dist[i] > THRESHOLD / 2:
                if index_dist[i+1] != 0 or index_dist[i+2] != 0:
                    first_match = False
                    flag_s = True
                    start = i
                    fstart = i
                    continue
        if index_dist[i] > THRESHOLD and not flag_s:
            if index_dist[i+1] != 0 or index_dist[i+2] != 0 or index_dist[i+3] != 0:
                flag_s = True
                start = i
                continue
        if flag_s:
            if index_dist[i] == 0 or index_dist[i+1] == 0:
                end = i
                flag_e = True
        tmp = ''
        if flag_e:
            for ii in xrange(start, end+1):
                if (len(lines[ii]) < 1): continue
                tmp += lines[ii] + '\n'
            main_text += tmp
            flag_s = flag_e = False

#    for pre in xrange(fstart - 1, max(0, fstart - BLOCKS_WIDTH), -1):
#        for md5 in images.keys():
#            if lines[pre].find(md5) > 0:
#                main_text = lines[pre] + '\n' + main_text
#                break

    for md5,img in images.iteritems():
        main_text = main_text.replace(md5, img)
    return strtotime(time), main_text

def parse(url, html):
    encoding, html = html_util.get_unicode_str(html)
    if encoding == '': return '', '', '', ''
    try:
        doc = lxml.html.document_fromstring(html)
        doc.make_links_absolute(url)
        html = lxml.etree.tounicode(doc, method='html')
    except:
        pass
    title, text = get_raw_info(html)
    
    time, text = get_main_content(text)
    return encoding, time, title, text

if __name__ == "__main__":
    html = open('index.html').read()
    encoding, time, title, text = parse('http://www.qq.com',html)
    print "编码："+encoding
    print '='*10
    print "标题："+title.encode('utf-8','ignore')
    print "时间："+time.encode('utf-8','ignore')
    print '='*10
    print "内容："+text.encode('utf-8','ignore')

