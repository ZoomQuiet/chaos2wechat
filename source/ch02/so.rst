.. include:: ../LINKS.rst


整个儿的
==============

最终,完成所有功能的配置和代码:



源代码
---------------------------
所有可运行代码如下

config.yaml
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml
    :linenos:

    ---
    name: wechat
    version: 3

index.wsgi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :linenos:
    :emphasize-lines: 2,3,5 

    # -*- coding: utf-8 -*-
    import sae
    import config
    from bottle import *
    from web import APP

    application = sae.create_wsgi_app(APP)




config.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :linenos:
    :emphasize-lines: 1,5-7,10,16,20-22,32

    # -*- coding: utf-8 -*-
    import sys
    import os.path

    app_root = os.path.dirname(__file__)
    sys.path.insert(0, os.path.join(app_root, "module/"))
    sys.path.insert(0, os.path.join(app_root, "web/"))

    class Borg():
        '''base http://blog.youxu.info/2010/04/29/borg
            - 单例式配置收集类
        '''
        __collective_mind = {}
        def __init__(self):
            self.__dict__ = self.__collective_mind
            
        TPL_TEXT=''' <xml>
         <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
         <FromUserName><![CDATA[%(fromUser)s]]></FromUserName>
         <CreateTime>%(tStamp)s</CreateTime>
         <MsgType><![CDATA[text]]></MsgType>
         <Content><![CDATA[%(content)s]]></Content>
         </xml>'''

    CFG = Borg()


web/__init__.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :linenos:
    :emphasize-lines: 4-5

    # -*- coding: utf-8 -*-
    from bottle import *

    APP = Bottle()
    APP.mount('/api', __import__('mana4api').APP)

    @APP.error(404)
    def error404(error):
        return template('404.html')

    @APP.route('/favicon.ico')
    def favicon():
        abort(204)
    


web/mana4api.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :linenos:
    :emphasize-lines: 4,6,8-9

    # -*- coding: utf-8 -*-
    import sae
    from bottle import *
    from config import CFG
    #debug(True)
    APP = Bottle()
    import sae.kvdb
    KV = sae.kvdb.KVClient()

    @APP.post('/echo')
    @APP.post('/echo/')
    def wechat_post():
        xml = etree.XML(request.forms.keys()[0])
        fromUser = xml.findtext("ToUserName")
        toUser = xml.findtext("FromUserName")
        __MsgType = xml.findtext("MsgType")
        __Content = xml.findtext("Content")
        tStamp = TSTAMP()
        if "text" == __MsgType:
            if "h" == __Content:
                content = "是也乎"
                return CFG.TPL_TEXT% locals()
            elif "i" == __Content:
                uid = hashlib.sha1(toUser).hexdigest()
                print uid
                usr = KV.get(uid)
                if None == usr:
                    # 首次应答,没有建立档案
                    pass
                else:
                    # 已经有档案
                    if "em" in usr.keys():
                        # 曾经记录过邮箱
                        content = "你的邮箱: %s"% usr['em']
                    else:
                        # 未记录过
                        content = "请输入你的邮箱如\nem:foo@bar.com"
                print CFG.TPL_TEXT% locals()
                return CFG.TPL_TEXT% locals()
            elif "em" in __Content.split(":"):
                uid = hashlib.sha1(toUser).hexdigest()
                usr = KV.get(uid)
                print __Content[3:]
                usr['em'] = __Content[3:]
                KV.replace(uid, usr)
                content = "你的邮箱: %s"% usr['em']
                print CFG.TPL_TEXT% locals()
                return CFG.TPL_TEXT% locals()

        return None 




应答逻辑
---------------------------

::

    -> h
    <- 是也乎

    -> i
    <- 请输入你的邮箱如\nem:foo@bar.com

    -> em:bar@gmail.com
    <- 你的邮箱: bar@gmail.com


但素!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


- 输入中文,是否可以判别?
- 成员想修改老的邮箱?
- 为毛不支持 `zoomquiet+gdg@gmail.com` 的 `+` 中缀邮箱?!
- 怎么查询过往活动?
- 如果想通过微信进行活动的报名?


.. note:: (~_~)

    - 所以! 这就是开发的乐趣,自个儿不断的制造需求,并解决问题!

