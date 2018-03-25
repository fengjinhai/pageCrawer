import hashlib

def md5(input):
    try:
        return hashlib.md5(input).hexdigest().lower()
    except:
        return ''
