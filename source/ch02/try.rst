.. include:: ../LINKS.rst


27:42" 重构
============================

根据文档, `SAE`_ 目前的服务基本覆盖了所有Web应用所需要的功能，包括：

- MySQL （分布式数据库服务，通过RDC提供）
- Memcache （分布式缓存服务）
- Storage（分布式文件存储服务）
- KVDB（分布式key-value持久化存储）
- Cron（分布式定时服务）
- Image（分布式图像处理服务）
- FetchURL（分布式网页抓取服务）
- Mail（分布式邮件服务）
- TaskQueue（异步轻量级任务队列）
- DeferredJob（异步大任务延迟队列）
- Counter（分布式计数器服务）
- Rank（实时排行榜服务）
...


当前小应用服务的加速需求其实就是:

- 每次来的查询,以查询的网址为键,在 `SAE`_ 中保存金山云查询结果
- 下次,再有查询,先检查,是否被查询过:

    - 如果有,立即本地搜索出来,返回请求
    - 如果没有,向金山云查询,并同樣保存一份儿

- 简单的説,就是个 `键-值` 对的本地数据库
- 对照一下,立即识别出 `KVDB` 就是对口的专门服务!


KVDB
---------------

`SAE Python 开发文档 <http://appstack.sinaapp.com/static/doc/release/testing/service.html#kvdb-tbd>`_ 中的示例代码 很简洁::

    import sae.kvdb

    kv = sae.kvdb.KVClient()

    k = 'foo'
    kv.set(k, 2)
    kv.delete(k)

    kv.add(k, 3)
    kv.get(k)

    kv.replace(k, 4)
    kv.get(k)

    print kv.get_info()


但是:

- `kv.get_info()` 吐出的都是什么含义?
- `KVDB` 中的键,有什么约定? 可以使用 url 嘛?
...

都没有进一步交待了,,, 好在通过 `Python`_ 可以快速完成探查,增补好功能!


调试
-----------------

根据示例代码,快速拼出一个功能函式: `qchk`

::

    @app.route('/qchk', method="POST")
    def qchk():
        url = request.forms.get('uri').split("/")
        if 1 == len(url):
            uri = url[0]
        else:
            uri = url[2]
        k = uri
        import sae.kvdb
        kv = sae.kvdb.KVClient()
        v = kv.get(k)
        print "kv.get(uri)~ type=%s var=%s"%(type(v),v)
        return "debugging..."


主要目标是想印证 `KVDB` 的使用,是否是自个儿想象的那样儿...

但是, `dev_server`_ 本地运行时, 一提交到 `localhost:8080/qchk/` 就囧掉:

::

    Traceback (most recent call last):
      File "/usr/local/bin/bottle.py", line 737, in _handle
        return route.call(**args)
      File "/usr/local/bin/bottle.py", line 1454, in wrapper
        rv = callback(*a, **ka)
      File "index.wsgi", line 57, in qchk
        import sae.kvdb
    ImportError: No module named kvdb
    127.0.0.1 - - [26/Apr/2012 11:42:28] "POST /qchk/ HTTP/1.1" 500 -


很明显, `dev_server`_ 中没有包含 `KVDB`_ 的模拟,,,

好吧,只有回到原始的调试过程:`修订->部署->对真实服务进行测试`

但是,真实运行中的服务,是跑在 `SAE`_ 中的,怎么看到为了调试,进行的 `print` 标准输出?


服务端日志
-----------------------------

好在 `SAE`_ 毕竟是商用 `PaaS`_ 服务! 当然有渠道可以观察的!

.. _fig_2_1:
.. figure:: ../_static/figs/chaos2-1-log.png

   插图 2-1 配合后台日志中心进行调试

如截屏所示...

- 每个版本的应用,都有具专用的日志收集渠道
- 日志的收集等级也详细分成5级
- 代码中的 `print` 调试信息,收集在 `debug` 级别日志通道中,,,

::

    print "kv.get(uri)~ type=%s var=%s"%(type(v),v)
                            |       |
                            |       +------------------------------------+
                            +------------------------------+             |
                                                           V             V
    [26/Apr/2012:14:31:56 +0800] kv.get(uri)~ type=<type 'NoneType'> var=None yf34 


对照调试代码,立即可以知道, `.get()` 在没有获取键值时,返回的是 `None`

那么立即就可以增进代码为完整的功能逻辑::

    @app.route('/qchk', method="POST")
    def qchk():
        url = request.forms.get('uri').split("/")
        if 1 == len(url):
            uri = url[0]
        else:
            uri = url[2]
        k = uri
        print k
        import sae.kvdb
        print "kv.get_info() %s"% kv.get_info()
        kv = sae.kvdb.KVClient()
        v = kv.get(k)
        print "kv.get(uri)~ type=%s var=%s"%(type(v),v)
        if None == v:
            result = _askCloud(cfg.APITYPE, uri)
            kv.add(k, result)
            return "/qchk(KSC)::\t %s" % cfg.PHISHTYPE[str(result)]
        else:
            return "/qchk(KVDB)::\t %s" % cfg.PHISHTYPE[str(v)]

即:
- 没有查到,说明是首次查询,那么正常的去问金山云
- 否则,就直接返回记录中的值

将代码部署上去后,自然的使用 `cURL`_ 从本地发出请求,如: :ref:`fig_2_2` :

.. _fig_2_2:
.. figure:: ../_static/figs/chaos2-2-curl.png

   插图 2-2 使用curl发送调试请求


对应的刷新日志页面, 情景如: :ref:`fig_2_3`

.. _fig_2_3:
.. figure:: ../_static/figs/chaos2-3-debug.png

   插图 2-3 调试请求的对应日志截屏


**BINGO!**



42:01" 小结
---------------------------------

~ 这一处增强,纯粹是根据文档配合后台日志,尝试几个回和而已,一刻钟,整出来不难吧?

- 但是,过程中的心理冲突,绝对不轻
- 比如,文档中未言明的各种细节, 是否重要? 怎么测试确认?
- 怎么设计 `print` 点输出的格式,以便从后台日志中明确的识别出?
- 等等,都需要补课,老实查阅文档,认真领悟,大胆尝试,建立靠谱的思路和反应,,,

不过,整体上,只要思路明确,方向正确,真心只是个轻松的过程而已,,,


.. note:: `KVDB`_ 的 `key`

    - 因为 `KVDB`_ 按文档吼,是对 `memcached`_ 接口的精简仿制;
    - 所以,根据 `Very long URL aliases not correctly cached in memcache <http://2bits.com/articles/very-long-url-aliases-not-correctly-cached-memcache.html>`_  等相关文章的分享,如果使用原样儿 URL 作 `key` 很可能出问题...
    - 笔者就曾经通过后台日志确认,只要使用正常的 URL 作 `key` 是保存不进 `KVDB`_ 的,
    - 于是使用 `urlsafe_b64encode(uri)` 进行处理就好...
    - 可是,没有想到 `SAE`_ 日新月异的发展中,现在再试,居然,平静的接受了! `叫声好!`


