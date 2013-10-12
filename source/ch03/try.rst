.. include:: ../LINKS.rst


再次重构
============================

追加新的有流程的指令前,要先解决一个问题: ``怎么在本地调试?!``

- 之前, 是通过 ``dev_server.py`` 提供的本地测试服务跑起来,
- 然后使用 `cURL`_ 在命令行上模拟微信发送来的消息 `XML`_

可是! 那是 `XML`_ 大堆大堆的标签,每次变动 ``指令`` 要在终端移动光标进行合理的修订,慢! 又容易出问题!

所以!

首先要有个命令行工具
---------------------------------

解决快速向本地测试服务发送吻合格式的测试请求!

进一步的说,就是可以根据简单的参数指定来组合出以下类似的命令,再执行::

    curl -d '[XML请求字串]' http://localhost:8080/api/echo   


而 ``[XML请求字串]`` 就是文档早已约定了的::

    <xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[fromUser]]></FromUserName>
    <CreateTime>1348831860</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[this is a test]]></Content>
    <MsgId>1234567890123456</MsgId>
    </xml>


每次本地测试时,嘦对 ``<Content><![CDATA[指令字串]]></Content>`` 进行替换而已


所以 ``CLI.py`` 就是:




.. code-block:: python
    :linenos:
    :emphasize-lines: 2-3,6,13-14,18

    # -*- coding: utf-8 -*-
    import sys
    from time import time
    from subprocess import Popen
    from xsettings import XCFG

    if __name__ == "__main__":
        if 2 != len(sys.argv):
            print """ Usage::
            $ python CLI.py [指令]
            """
        else:
            TPL_TEXT='''<xml>
            <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
            <FromUserName><![CDATA[%(fromUser)s]]></FromUserName>
            <CreateTime>%(tStamp)s</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[%(content)s]]></Content>
            </xml>'''

            toUser = XCFG.AS_SRV
            fromUser = XCFG.AS_USR

            tStamp = int(time())
            content = sys.argv[1]
            xml = TPL_TEXT % locals()

            cmd = "curl -d '%s' http://localhost:8080/api/echo"% xml
            print cmd
            #Popen(cmd, shell=True, close_fds=True)


是的,就这样,就解决了一个现实的问题::

    $ python chaos_CLI.py
     Usage::
            $ python CLI.py [指令]

    $ python chaos_CLI.py h
    $ python chaos_CLI.py s
    ...

使用时,就将要发送到服务端的复杂的 `XML`_ 消息模拟,变成了只要变更指令本身就好!


唯一的技巧
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``from xsettings import XCFG``

意思,就是关键的涉及安全的参数,不进入开源仓库, 使用专门的配置文件进行管理,
形式上完全类似前述在使用的 ``config.py``

当然的, 使用 `GitHub`_ 时,要对应配置 ``.gitignore`` ::

    .ropeproject
    *.dump
    *.pyc
    *.db
    *.log
    .svn
    .DS_Store
    *.wsgic
    logs
    xsettings.py


追加 ``xsettings.py``




改造指令响应函式
---------------------------------
再来看一下

`web/mana4api.py` 关键部分已经扩展为:


.. code-block:: python
    :linenos:
    :emphasize-lines: 1-2,17,18,20,34-39

    import sae.kvdb
    KV = sae.kvdb.KVClient()
    #...
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



先来尝试将设想中的文章查阅逻辑加到这个越来越长的 ``if elif else`` 判定树中:


.. code-block:: python
    :linenos:
    :emphasize-lines: 1-2,17,18,20,34-39

    #...
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
            elif "s" == __Content:
                #进入查询流程
                pass
            elif "dd" == __Content:
                # 进入查询 dd ~ D码点评分类列表
                pass
            elif "某个文章编号" == __Content:
                # 进入输出指定分类文章中具体文章图文链接
                pass
            elif "i" == __Content:




.. warning:: (\\o/)|||

    - 停!!!!


if else 无能为力!
---------------------------------


.. _fig_3_2:
.. figure:: ../_static/figs/chaos3-2-gdg_seek_words.png

   插图 3-2 如果包含一个支持随时退出流程的 ``*`` 指令


其实整个查阅公众号过往文章的业务,和一般的电话银行业务是没有什么不同的,

所以,也可以自然的追加一个 ``*`` 指令,退回上级菜单,或是退出查阅流程.

一般的条件判定结构: ``if elif else`` 对此是完全无力的:

- 因为公众号的应答,完全同web 网站的反馈
- 每次不同的成员输入指令,对于服务端而言都是全新的,独立的一次请求
- 服务端虽然可以识别用户,但是,用户上次输入了什么指令,以及指令序列的上下文,是无法通过简单的条件判定来得出的
- 因为成员是人,是人就会出错, 而且在移动端,什么情况都会发生,要想确保流程稳定可用,就需要预先对所有情况都加以判定!

想想都是个麻烦的事儿!





**BazingA**

那肿么办呢....

