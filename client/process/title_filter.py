import re

def removesuffixcommon(inputstr, label):
    pos = inputstr.rfind(label)
    if pos > 0.5 * len(inputstr):
        return inputstr[ : pos]
    return inputstr

def removeprefixcommon(inputstr, label):
    pos = inputstr.find(label)
    if pos != -1 and pos < 0.5 * len(inputstr):
        return inputstr[pos+len(label) : ]
    return inputstr
    
def getlongest(inputstr, label):
    strs = inputstr.split(label)
    restr = ''
    for strone in strs:
        if len(strone) > len(restr):
            restr = strone
    return restr
        

def filt(inputstr):
    title = getlongest(inputstr, ' | ')
    title = removeprefixcommon(title, ' | ')
    title = removeprefixcommon(title, ' - ')
    title = removeprefixcommon(title, ' : ')
    title = removesuffixcommon(title, ' - ')
    title = removesuffixcommon(title, ' | ')
    title = removesuffixcommon(title, ' : ')
    return title

def remove(inputstr):
    title = inputstr
    title = re.sub(ur".*<.*>.*", '', title)
    title = re.sub(ur".*\|.*\|.*\|.*", '', title)
    title = re.sub(ur".*,.*,.*", '', title)
    title = title.replace(u'\xa0', u' ')
    return title
