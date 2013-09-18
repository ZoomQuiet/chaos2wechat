# -*- coding: utf-8 -*-
VERSION = "urisaok v11.12.28"
import sae
import urllib2 as urilib
from bottle import Bottle, request
app = Bottle()

@app.route('/')
def hello():
    return '''%s powerded by Bottle + SAE !
    usage:
    $ curl -d 'uri=http://sina.com' 1.urisaok.sinaapp.com/chk/
        '''% VERSION

@app.route('/chk/', method="POST")
def chk():
    uri = request.forms.get('uri')
    print uri
    result = _askCloud(APITYPE, uri)
    return "/chk %s"% result

import base64
import time
from hashlib import md5
APPKEY = "k-60666"
SECRET = "99fc9fdbc6761f7d898ad25762407373"
OPEN_HOST = "open.pc120.com"
APITYPE = "/phish/"
PHISHTYPE = {'-1':'未知'
    ,'0':'非钓鱼'
    ,'1':'钓鱼'
    ,'2':'网站高风险,有钓鱼嫌疑'
    }

def _askCloud(api_path, url):
    args = __genQueryArgs(api_path, url)
    api_url = "http://%s%s?%s"% (OPEN_HOST, APITYPE ,args)
    print api_url
    result = eval(urilib.urlopen(api_url).read())
    print result
    if result['success'] == 1:
        doc = result['phish']
        return "%s:: %s"% (doc, PHISHTYPE[str(doc)])
    else:
        return result

def __genQueryArgs(api_path, url):
    args = "appkey=" + APPKEY
    args += "&q=" + base64.urlsafe_b64encode(url)
    args += "&timestamp=" + "%.3f" % (time.time())
    sign_base_string = api_path + "?" + args
    args += "&sign=" + md5(sign_base_string + SECRET).hexdigest()
    return args

application = sae.create_wsgi_app(app)