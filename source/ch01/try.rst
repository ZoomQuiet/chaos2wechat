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








27:00" 小结
---------------------------

以上这一小堆代码,二十分钟,整出来不难吧? 因为,基本上没有涉及太多 `Bottle`_ 的特殊能力,
几乎全部是标准的本地脚本写法儿,想来:

