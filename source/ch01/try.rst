.. include:: ../LINKS.rst


7:42" 突入 
==============

嗯嗯嗯,现在可以开始计时了...


本地运行
---------------------------

要提高开发效率 , 当然是在本地有个真实环境,可以就地调试 ,免去每次修订,都要上传 `SAE`_ 的时间

- 事实上 `GAE`_ 从刚开始就是这么整的,发布有 SDK,包含本地模拟环境
- `SAE`_ 的 `dev_server`_ 也是作这事儿的!

如: :ref:`fig_1_2` 所示:

- 默认守护 `8080` 端口,当然,可以自行指定
- 美好的是, `dev_server`_ 能够感知到 `index.wsgi` 的变化,自动重启!


.. _fig_1_2:
.. figure:: ../_static/figs/chaos1-2-devsrv.png

   插图 1-2 使用dev_server.py



Bottle
---------------------------

.. sidebar:: 什么是框架?
    :subtitle: ~web应用框架

    - 首先, `Python`_ 世界中 `Web框架超级多! <http://wiki.python.org/moin/WebFrameworks>`_
    - 为毛? `Python Web应用框架纵论 <http://wiki.woodpecker.org.cn/moin/ObpLovelyPython/PCS304>`_ 有分析
    - 不过, 框架到底是什么? 和模块有什么区别?
    - `CPyUG`_ 的列表中争论过多次,最后的共识是: `框架是种可复用的设计构件!`  给人用的,包含丰富过往经验的,内置多种领域常见功能的,加速应用开发的专用模块集...


`SAE`_ 支持多种 web 应用框架, 不过, 对于 0基础的人而言, 推荐先从 `Bottle`_ 开始体验 ;-)

- `Docs - Bottle 0.8 中文 <http://floss.zoomquiet.org/data/20100902150939/index.html>`_
- 以及 `Bottle初学者 TODO-list 实例导引 — Bitbucket <https://bitbucket.org/ZoomQuiet/bottle-simple-todo/wiki/GudierFresher>`_

事实上, `SAE`_ 官方文档中,各种 web 应用框架的 `Hallo World` 也是 `Bottle`_ 的最短:

::

    import sae
    from bottle import Bottle, run

    app = Bottle()
    @app.route('/')
    def hello():
        return "Hello, world! - Bottle"
    application = sae.create_wsgi_app(app)

需要理解的,其实就其中3行(其它都是约定的八股文,照抄就好;-)::

    @app.route('/') # 访问路由,截获对根 URL 的访问
    def hello():    # 以函式来进行真实的执行处理
        return "Hello, world! - Bottle"
        # 最后統一使用 return 返回请求给用户



URIsAok
-----------------------

对于,我们的目标任务: 包装 `金山网址云安全开放API <http://code.ijinshan.com/api/devmore4.html#md1>`_ 为 `REST`_ 在线服务; 

不用研究透 `Bottle`_ ,仅仅需要作到以下几点,就可以完成核心功能了:

- 对指定 URL 接收 `POST` 方式提交来的待查网址
- 根据文档, 对查询参数项进行合理的 `base64` / `md5` 编码
- 对金山网址云,发起合理请求,并收集结果


完成后的使用效果, 如 :ref:`fig_1_3` 

.. _fig_1_3:
.. figure:: ../_static/figs/chaos1-3-chk.png

   插图 1-3 完成 /chk/ 功能


整体代码,不过 50几行...


.. literalinclude:: index.py
    :language: python
    :linenos:




关键行为代码:

- 接收 `POST` 数据 ::

    @app.route('/chk/', method="POST")  # 路由声明中,可以追加提交方式的规定
    def chk():
        uri = request.forms.get('uri')  # 内置的 request.forms 对象专门进行提交数据处理的

- 合理进行参数处理::

    args += "&q=" + base64.urlsafe_b64encode(url)   # url安全的base64编码
    args += "&timestamp=" + "%.3f" % (time.time())  # 时间戳
    sign_base_string = api_path + "?" + args
    args += "&sign=" + md5(sign_base_string + SECRET).hexdigest() # md5编码

- 向云服务查询,并收集结果::

    import urllib2 as urilib
    ...
    result = eval(urilib.urlopen(api_url).read())
               |            |       |       +- 返回数据当成文件对象读取出
               |            |       +-- 组合好的查询url
               |            +-- 内建的外访函式
               +-- 返回的是 JSON 格式数据,兼容 Py 的dict 对象,所以,可以就地转换





27:00" 小结
---------------------------

以上这一小堆代码,二十分钟,整出来不难吧? 因为,基本上没有涉及太多 `Bottle`_ 的特殊能力,
几乎全部是标准的本地脚本写法儿,想来:

- 其实,关键功能性行为代码,就8行

    - 仅仅有一行,是需要钻研文档的,,,
    - 即: `eval(urilib.urlopen(api_url).read())`

.. _fig_1_4:
.. figure:: ../_static/figs/chaos1-4-urllib.png

    插图 1-4 访问外网的涉及文档

    - 之前版本文档中,吼关闭了多数对外访问的模块,只能使用 `urllib2`
    - 后来 `SAE`_ 的快速进化,又重新开放了主要的常见几个对外网络访问的库模块 
    - 但是,没有例子,没有推荐链接,真心一句话,是很需要心灵感应才知道怎么作的..

- 其余,都是力气活儿

    - 只要别抄錯
    - 都是赋值,赋值,赋值,赋值,,,,

- 只要注意每一步,随时都可以使用 `print` 吼回来,测试确认无误,就可以继续前进了,,,

`这就是脚本语言的直觉式开发调试体验!`

