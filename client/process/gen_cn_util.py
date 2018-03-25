out = open('cn_util.py','w')
out.write("#encoding=utf-8\n")
out.write("g_popular_cn_word = set([\n")
for line in open('popular_word.txt'):
    line = line.strip().decode('gbk').encode('utf-8')
    out.write("    u'%s',\n" % line)
out.write("])\n")
out.close()
