# -*- coding: utf-8 -*-

import urllib

def makeTiny(url):
    url='http://tinyurl.com/api-create.php?'+urllib.urlencode({'url':url})
    return urllib.urlopen(url).read()
