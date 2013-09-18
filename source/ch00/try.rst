.. include:: ../LINKS.rst


00:00" 初尝
==============

整起来先!
- 嗯嗯嗯,现在可以计时了: `00:00`

安装
--------

`参考:` `dev_server`_ 官方安装说明


.. sidebar:: 提示

    - 不专门说明的话,指的都是笔者的个人环境:

      - MacOS X 10.7.3
      - `Python`_ 2.7.1

    - 不过,真心兼容所有 Linux 发行版环境的!
    - 另外在引用中文本中:
    - `$` 表示以普通用户,在命令行环境中的操作;
    - `#` 表示以`root`身份,在命令行环境中的操作;


安装SAE本地虚拟环境 ::

    $ git clone http://github.com/SAEPython/saepythondevguide.git
    $ sudo python setup.py install
    $ dev_server.py --help
    Usage: dev_server.py [options]

    Options:
      -h, --help            show this help message and exit
      -p PORT, --port=PORT  Which port to listen
      --mysql=MYSQL         Mysql configuration: user:password@host:port
      --storage-path=STORAGE
                            Directory used as local stoarge


同时也就拥有了SAE专用部署工具 `saecloud`_ ::


    $ saecloud version
    SAE command line v0.0.1
    $ saecloud -h
    usage: saecloud [-h] {version,export,deploy} ...

    positional arguments:
      {version,export,deploy}
                            sub commands
        export              export source code to local directory
        deploy              deploy source directory to SAE
        version             show version info

    optional arguments:
      -h, --help            show this help message and exit




创建
--------

参考 :ref:`fig_0_1` ,首先通过 `邀请码`_ ,进入 `SAE`_ 后台;

.. _fig_0_1:
.. figure:: ../_static/figs/chaos0-1.png

   插图 0-1 创建SAE应用


- 然后从 `我的首页->创建新应用` 进入;
- 完成全新 `Pyhton`_ 应用的命名与创建...
- 当前乱入为例, 创建的是 `urisaok`


.. note:: 注意!

    选择开发语言为 `Python`_ ,才好进一步的各种乱入...




初玩
----------

那么开始 `SAE`_ 的应用编程吧!

理解 `SAE`_ 的应用目录结构::

    /path/2/you/urisoak/
      +- config.yaml    应用配置
      +- index.wsgi     应用根代码


94这么简单!

当然,要从 `Hallo World` 开始品尝!

`index.wsgi`::

    import sae

    def app(environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return ['Hello, world!']

    application = sae.create_wsgi_app(app)



`config.yaml`::

    ---
    name: urisaok
    version: 1
    ...

完成以上仅仅两个文件的创建,以及修订(完全从官方 `快速指引 <http://appstack.sinaapp.com/static/doc/release/testing/quickstart.html>`_ 抄来就好)

然后使用 `saecloud`_ 完成部署 ::

    $ saecloud deploy
    Deploying http://1.urisaok.sinaapp.com
    Updating cache
    Finding changes
    Pushing to server...  done


就类似 :ref:`fig_0_2` ,明确当前的应用运行情况!

.. _fig_0_2:
.. figure:: ../_static/figs/chaos0-2-apps.png

   插图 0-2 应用版本在后台


.. note:: (~_~)

    此处,因为大妈,曾经部署过两个版本,所以截屏可能同读者处看的有点不同;

    不过,可以直观的明确 `SAE`_ 应用版本限定:

      - 每个应用最多有 10 个版本
      - 以版本 x 为例,应用的访问 URL 是:

        - `http://x.应用名.sinaapp.com/`

      - 每次可以指定唯一己在线版本为正式发布版本, URL为:

        - `http://应用名.sinaapp.com/`


推荐使用 `cURL`_ 进行测试::

    $ curl -v 1.urisaok.sinaapp.com 
    * About to connect() to 1.urisaok.sinaapp.com port 80 (#0)
    *   Trying 220.181.136.234... connected
    * Connected to 1.urisaok.sinaapp.com (220.181.136.234) port 80 (#0)
    > GET / HTTP/1.1
    > User-Agent: curl/7.21.4 (universal-apple-darwin11.0) libcurl/7.21.4 OpenSSL/0.9.8r zlib/1.2.5
    > Host: 1.urisaok.sinaapp.com
    > Accept: */*
    > 
    < HTTP/1.1 200 OK
    < Server: nginx/1.1.0
    < Date: Wed, 25 Apr 2012 13:57:24 GMT
    < Content-Type: text/plain
    < Connection: close
    < Set-Cookie: saeut=14.117.42.241.1335362244745161; path=/; max-age=311040000
    < Via: 10.73.26.28
    < Content-Length: 13
    < 
    * Closing connection #0
    Hello, world!

可以方便的完整观察到整个 http 请求的过程,,,



小改
--------

推荐类似 :ref:`fig_0_3` ,布置好本地开发环境 ;-)

.. _fig_0_3:
.. figure:: ../_static/figs/chaos0-3-tmux.png

   插图 0-3 tumx合理配置的本地开发调试界面


- 笔者推荐 `tmux`_ 作窗口管理,可以快速根据需求分割同时,将整个开发过程完备的显示出来,而且:

  - 自动保存所有窗口状态,如果意外断线,或是 shell 关闭
  - 下次使用 `tmux a -t 0` 就恢复第 `0` 个 `tumx`_ session 的所有窗口

- 当前是,顶部,进行 `saecloud`_ 操作
- 左下,进行代码修订
- 右下,进行版本管理以及测试操作



7:01" 小结
------------------

不出意外的话, 七分钟 用在这个阶段,很足够了!


整体思路,就是要,先习惯,并建立起,依托 `SAE`_ 的开发过程:

::

      修订代码
      ^  `->saecloud deploy
      |       `-> curl 请求测试
      |               |
      +---------------/



