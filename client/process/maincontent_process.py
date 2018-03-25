import re
from tld import get_tld

import html_util

# <meta property="og:image"
RE_OGIMAGE_CONTENT = ur'(?is)<meta\s+property=[\"\']og:image[\"\'][^\/>]*content=[\"\'](.*?)[\"\'].*?/>' 
RE_OGIMAGE = ur'(?is)<meta\s+property=[\"\']og:image[\"\'][^\/>]*content=[\"\'].*?[\"\'].*?/>' 

RE_IMG = ur'(?is)(<img.*?>)'
RE_IMG_SRC = ur'(?is)<img.+?src=[\'\"](.+?)[\'\"].*?>'
RE_HEAD = ur'(?is)<head.*?>(.*?)<\/head>'
RE_TAG = ur'(?is)<.*?>'

def removeduplicate(text):
    retext = text
    #remove duplicate
    imagespat = re.findall(RE_IMG, text)
    for imagepat in imagespat:
        images = re.findall(RE_IMG_SRC, imagepat)
        if len(images) == 0:continue
        image = images[0]
        if retext.count(image) > 1:
            retext = retext.replace(imagepat, '', retext.count(image) - 1)
    return retext

def supplementalimages(html, text):
    if text == '':return text
    #meta images
    images = re.findall(RE_OGIMAGE, html)
    #print "####meta images:%s"%images

    filtwords = ['thumbnailurl', 'logo']
    #if meta image has already in text,continue
    imagetext = ''
    for image in images:
        #filt
        bfind = False
        for filtword in filtwords:
            if image.lower().find(filtword) != -1:
                bfind = True
                break
        if bfind : continue

        t_image = re.findall(RE_OGIMAGE_CONTENT, image)
        if len(t_image) == 0:continue
        image = t_image[0]
        if text.find(image) == -1:
            #<img src=\"http://media2.intoday.in/indiatoday/images/stories/cars-video_305_120415044702_120615122434.jpg\" />\n
            imagetext += '<img from=\"meta\" src=\"' + image + '\" />\n'
            #print "######add imagetext:\n%s"%imagetext

    return imagetext


def supplesubtitleimages(url, html, text, title):
    if text == '':return text
    imagetext = ''

    try:
        bodytext = re.sub(RE_HEAD, '', html)

        #subtitle
        titlepos = (html_util.unescape(bodytext)).find(title)
        if titlepos >= 0:
            bodytext = bodytext[titlepos : ]
        #print "bodytext:%s"%bodytext[:1000]
        
        #upcontent
        contentpos = -1
        text1 = re.sub(RE_TAG, '', text)
        if len(text1) > 30:
            lastcontent = text1[len(text1) - 30 : ]
            contentpos = (html_util.unescape(bodytext)).find(lastcontent)
        if contentpos > 0:
            bodytext = bodytext[ : contentpos]

        #domain
        domain = ''
        try:
            domain = get_tld(url)
            #print "domain:%s"%domain
        except Exception, e:
            print e
            pass
        
        #words
        keywords = ['.jpg', '.gif', '.jpeg']
        filtwords = ['thumb', 'twitter', 'facebook']

        images = re.findall(RE_IMG_SRC, bodytext)
        for image in images:
            #domain
            if image.find(domain) < 0 and image.lower().find('news') < 0 \
                    and image.find('intoday') < 0 and image.startswith('/') == False:
                continue

            #one keyword at least
            bfind = False
            for keyword in keywords:
                if image.lower().find(keyword) != -1:
                    bfind = True
                    break
            if bfind == False:
                continue

            # no filtword
            bfind = False
            for filtword in filtwords:
                if image.lower().find(filtword) != -1:
                    bfind = True
                    break
            if bfind:
                continue

            if image.lower().startswith('/') :
                if domain.find('http://') == -1:
                    image = 'http://' + domain + image 
                else:
                    image = domain + image 


            imagetext += '<img from=\"subtitle\" src=\"' + image + '\" />\n'
            break

    except Exception, e:
        print e
        pass

    return imagetext

def suppleimages(url, html, text, title):
    if text == '':return text
    retext = text

    try:
        #exist image,then return
        if len(re.findall(RE_IMG_SRC, text)) > 0:return text

        #imagetext in front of text
        imagetext = ''
        if imagetext == '':
            imagetext = supplementalimages(html, text)
        if imagetext == '':
            imagetext = supplesubtitleimages(url, html, text, title)

        retext = imagetext + text
    except Exception, e:
        print e
        pass

    return retext

def filtimages(url, text):
    if text == '':return text
    retext = text

    try:
        #domain
        domain = ''
        domain = get_tld(url)

        retext = removeduplicate(retext)

        #key words
        filtwords = ['.png', 'logo', 'print', 'bookmark', 'email', 'author', 'default', 'actit.gif']
    
        imagespat = re.findall(RE_IMG, retext)
        for imagepat in imagespat:
            images = re.findall(RE_IMG_SRC, imagepat)
            if len(images) == 0:continue
            image = images[0]
            bfind = False
            for filtword in filtwords:
                if image.lower().find(filtword) != -1:
                    bfind = True
                    break
            if image.startswith('/') == True or image.startswith('admin') == True:
                if domain.find('http://') == -1:
                    image1 = 'http://' + domain + '/' + image
                else:
                    image1 = domain + '/' + image

                retext = retext.replace(image, image1)
                imagepat = imagepat.replace(image, image1)
                image = image1
            if image.find(domain) == -1 or bfind :
                retext = retext.replace(imagepat, '')
    except Exception, e:
        print e
        pass

    return retext

def processimages(url, html, text, title):
    if text == '':return text

    retext = text

    try:
        text = filtimages(url, text)
        retext = suppleimages(url, html, text, title)
        retext = removeduplicate(retext)
    except Exception, e:
        print e
        pass

    return retext
