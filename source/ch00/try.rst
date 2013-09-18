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





初玩
----------

那么开始 `SAE`_ 的应用编程吧!

理解 `SAE`_ 的应用目录结构::

    /path/2/you/urisoak/
      +- config.yaml    应用配置
      +- index.wsgi     应用根代码


94这么简单!


推荐使用 `cURL`_ 进行测试::



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



