import jpype
import os
import glob
import json

'''
jvmPath = jpype.getDefaultJVMPath()
path = os.path.dirname(os.path.abspath(__file__))
jars = glob.glob("%s/plato/lib/*.jar" % path)
jvmArg = "-Djava.class.path=%s" % ':'.join(jars)
if not jpype.isJVMStarted():
    jpype.startJVM(jvmPath,'-ea',jvmArg)
SilentSimpler = jpype.JClass("com.baidu.global.mobile.hao123.toolkit.plato.simplers.SilentSimpler")
'''
def silent(html):
    jvmPath = jpype.getDefaultJVMPath()
    path = os.path.dirname(os.path.abspath(__file__))
    jars = glob.glob("%s/plato/lib/*.jar" % path)
    jvmArg = "-Djava.class.path=%s" % ':'.join(jars)
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath,'-ea',jvmArg)
    SilentSimpler = jpype.JClass("com.baidu.global.mobile.hao123.toolkit.plato.simplers.SilentSimpler")
    simpler =  SilentSimpler(html, json.dumps({}))
    content = simpler.getPageContent()
    return content

def stander(url):
    jvmPath = jpype.getDefaultJVMPath()
    path = os.path.dirname(os.path.abspath(__file__))
    jars = glob.glob("%s/plato/lib/*.jar" % path)
    jvmArg = "-Djava.class.path=%s" % ':'.join(jars)
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath,'-ea',jvmArg)
    StanderSimpler = jpype.JClass("com.baidu.global.mobile.hao123.toolkit.plato.simplers.StanderSimpler")
    title = ''
    content = ''
    try:
        simpler =  StanderSimpler(url)
        content = simpler.getPageContent()
        title = simpler.getPageTitle()
    except jpype.JavaException, ex:
        print ex.javaClass(), ex.message()
        print ex.stacktrace()
    return title,content

if __name__ == "__main__":
    # packData = {
    # "url" : "br.noticias.yahoo.com/destaque-segunda-divis%C3%A3o-espanhola-atacante-negocia-clubes-elite-191208335--spt.html",
    # "pub-time" : "21/09/2014 11h15 ",
    # "html" : open("test/t.html").read().decode('windows-1252'),
    # "main-pic" : "http://assets.kompas.com/data/photo/2014/06/24/00215621561780x390.jpg?t=o&v=300",
    # }
    #ret = silent(open("1.html").read().decode('utf-8'))
    #print ret.encode('utf-8')
    #ret = stander('http://www.hindustantimes.com/india/experts-suggest-collegium-system-must-be-transparent/story-LAT8VeLEXCa1Qrd9Ue1S3I.html')
    url = "http://news.detik.com/berita/2737274/puan-harap-kisruh-di-dpr-cepat-selesai"
    url = "http://www.oneindia.com/international/over-40-percent-china-online-goods-shoddy-counterfeit-report-1916875.html"
    url = "http://www.desimartini.com/news/kannada/priyamani-would-love-direct-sudeep/article26337.htm"
    url = "http://www.filmibeat.com/television/news/2015/bigg-boss-9-rishabh-mandana-target-kishwer-next-task-203991.html"
    url = "http://carsizzler.com/news-detail/003839/VW-to-showcase-its-upcoming-compact-sedan-at-the-2016-Indian-Auto-Expo.html?utm_source=exit&utm_medium=web&utm_campaign=smartexit"
    url = 'http://www.businesstoday.in/markets/company-stock/why-tree-house-surged-10percent-after-hitting-52-week-low/story/226602.html'
    url = 'http://www.deccanchronicle.com/151201/sports-cricket/article/i-think-it-big-eye-opener-waqar-younis-pakistan%E2%80%99s-t20-loss'
    url = 'http://www.deccanchronicle.com/151217/lifestyle-offbeat/article/princess-diana%E2%80%99s-wedding-cake-will-soon-be-auctioned-4000'
    #ret = stander('http://finance.ifeng.com/a/20151103/14052832_0.shtml')
    title,ret = stander(url)
    print url
    print title.encode('utf-8')
    print ret.encode('utf-8')
