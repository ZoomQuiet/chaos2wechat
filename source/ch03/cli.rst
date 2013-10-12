.. include:: ../LINKS.rst


CLI
==============

经过本地测试,一切响应正当了,就遇到一大波躲不了的为了持续运营的:

非功能性需求
---------------------------------

- `非功能性需求 <http://zh.wikipedia.org/zh-cn/%E9%9D%9E%E5%8A%9F%E8%83%BD%E6%80%A7%E9%9C%80%E6%B1%82>`_ ! 比如:
    - 如何 快速检查运行中的远程系统健康情况?
    - 如何 批量增加/初始化 文章数据?
    - 如何 指定增补/修订 文章数据?
    - 如何 备份远程系统中的关键数据?
    - 如何 从本地恢复远程系统中的关键数据?
    - ...
- 更加蛋痛的是,如果在 `SAE`_ 上开发专用的管理员界面,那么:
    - 页面设计
    - 文件上传
    - 用户认证
    - 安全防护
    - ...
- 无穷无尽的全新功能就要开发!
    - 完全为几个管理员可以安全/顺利的在网页中进行数据管理 使用而已
    - 值得嘛?
    - 这时,才想起来 `Django`_ 内置的管理员界面早已内置了所有数据管理的功能
    - 可素! 我大 `Django`_ 是要用 ``MySQL`` 的, OMG 这货是更加无穷无尽的坑了!




何以解忧? 唯有CLI !
---------------------------------

`CLI`_ ~ Command-Line Interface 命令行用户界面

- 参考: `完全用命令行工作-5: 完结篇 « 4G spaces <http://blog.youxu.info/2009/07/22/cli-2/>`_ 系列文章
- 就能感受到, `CLI`_ 在明白人儿心中的无上享受!


关键是:

- `CLI`_ 的爽利环境要靠谱的操作系统配合, 必须是 Linux 或是 MAC, 这天然的决定了只会 M$ Windows 的麻瓜是无法使用的,即,只有靠谱的人,明白自个儿在作什么的人, 才能使用,无形中,将使用者这一端的安全隐患给杀灭了一大波!
- `CLI`_ 运行在伟大的 `Shell <http://zh.wikipedia.org/zh-cn/Unix_shell>`_ 环境中,天然的有良好的软件包管理服务支撑,太多常用/实用/高效/安全 的数据处理工具,可以简单的快递安装,直接调用,根本不用自个儿再开发了!
- `CLI`_ 的文字界面,不用 HTML/JS/CSS 来排版,简洁无比,但是,可以组合起来,快速完成丰富的任务!



安全性
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

首先要解决的是, 公众号应答系统是开源的呵!

``如何在代码开源的情况下,确保系统访问的安全?!``

- 介事儿,看起来高端,其实,运用简单的加密原理也就可以了!
- 参考: `42分钟乱入 SAE 手册!-) <http://chaos2sae.readthedocs.org/en/latest/>`_
    - 其中提及的 金山云安全网址查询接口的加密方式, 已经在以往的小应用中实现过:
    - `ZoomQuiet / ok.URIsA / source / index.wsgi — Bitbucket <https://bitbucket.org/ZoomQuiet/ok.urisa/src/e5437ca289516bc23345b9ebe3a10ad6232120f4/index.wsgi?at=SAE>`_
    - 可以拿来直接用!

原理也很简单:

1. 为了证明是一次安定团结的合理请求
    - 每次发送网络请求前
    - 要将必要的请求参数以及时间戳和约定好的 ``APPKEY`` 以固定的顺序组合成一个字串
    - 再加上事先准备的 ``SECRET`` 字串(即俗称的 `加盐 <http://zh.wikipedia.org/zh-cn/%E7%9B%90_(%E5%AF%86%E7%A0%81%E5%AD%A6)>`_)
    - 组合起来后进行 ``md5`` 散列,得出安全码
    - 将安全码作为 ``sign`` 签名字段附加在正当的请求中
2. 而在服务端口
    - 有事先约定的 ``APPKEY`` 以及 ``SECRET``
    - 又能从请求中获得 时间戳
    - 就可以将安全码的运算同样进行一次,得到的字串同提交上来的 ``sign`` 进行对比
    - 一致就说明是从正确的客户端发送来的
    - 再对比时间戳,在约定的时间范围内的算合法,比如,可以设定为 ``0.42秒`` 之内
    - 然后才算通过检验,进入正当的数据处理/响应!


那么,只要 ``APPKEY`` 以及 ``SECRET`` 不泄露:

- 攻击者,即使截获了相关请求的数据
- 也无法伪造出相应的请求签名来
- 如果使用穷举/彩虹字典等等方式来探查所有字串的可能,也无法在规定的安全时限中完成


RESTful
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`RESTful`_ 是种很好的接口设计思路!

而且 `Bottle`_ 支持 `RESTful`_ 约定的多种标准 http 请求形式, 简单到变化不同的声明就好,
比如::

    @APP.get('/cli/revert/<matter>')
    ...
    @APP.put('/cli/revert/<matter>')
    ...
    @APP.post('/cli/revert/<matter>')
    ...
    @APP.delete('/cli/revert/<matter>')


`RESTful`_ 将所有请求路径,以及数据集,以一种 ``表述性状态转移`` 的态度应对,
从而,获得了数据操作的合理/优雅的指代,并通过 http 的标准操作的区分,
能自然的对系统进行合理的分布式扩展!

好吧,以上可以算梦话,可以忽略!

关键是发现了无上萌物:

- `jkbr/httpie <https://github.com/jkbr/httpie>`_  cURL-like tool for humans
- 以及各种小伙伴的惊喜体验:`[httpie] - アルパカDiary <http://d.hatena.ne.jp/toritori0318/searchdiary?word=%2A%5Bhttpie%5D>`_

对应发出以上 `RESTful`_ 请求的形式类似::

    $ http GET http://我们的应答系统/api/cli
    $ http DELE http://我们的应答系统/api/cli
    $ http -f PUT http://我们的应答系统/api/cli
    $ http -f POST http://我们的应答系统/api/cli
    $ http -f POST http://我们的应答系统/api/cli json@path/2/本地文件


最后一个形式,就是模拟网页表单的文件提交::

    <form enctype="multipart/form-data" 
        method="post" 
        action="http://我们的应答系统/api/cli">
        <input type="file" name="json" />
    </form>



CLI 的交互参数
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

好吧,随着应答功能的追加, 对应的运营用 `CLI`_ 的维护命令也会越来越多!

- 对应的,命令行参数形式也会快递增加!
- 这也就存在一个如何 `Pythonic`_ 的解析 `CLI`_ 参数的问题!

果然,这种常见事务,在 `Pythonic`_ 也是大堆的同类模块:

- `hfeeki/cmdln <https://github.com/hfeeki/cmdln>`_
- `argparse – Command line option and argument parsing. - Python Module of the Week <http://pymotw.com/2/argparse/>`_
- `OptionParser -- 处理选项 <http://jianlee.ylinux.org/Computer/Python/OptionParser.html>`_
- `13.2. ConfigParser — Configuration file parser — Python v2.7.5 documentation <http://docs.python.org/2/library/configparser.html>`_
- `whtsky/parguments <https://github.com/whtsky/parguments>`_
- `halst/docopt <https://github.com/halst/docopt>`_
- ...

继续,动用在 `github`_ 中锻炼出来的同类模块选择方式:

1. 看官方网站是否可访问
2. 看官方文档是否完备
3. 尝试在一刻钟之内,是否可以根据文档+示例,完成一个小实例!

再加上小伙伴们的口碑,果断是 `halst/docopt <https://github.com/halst/docopt>`_ 了!

参考官网的样例: `docopt—language for description of command-line interfaces <http://docopt.org/>`_

就知道为毛这么多人用了就不撒手了!

- 因为 ``docopt`` 正如其名, 直接用模块的自述文本来作为输出的提醒帮助以及同时作为参数项目解析的定义了!!!
- 写一段文字,完成两件事儿,这简直就是 `Pythonic`_ 的完美诠释哪!
- 而且,所有参数的解析匹配,最后统一给到一个字典里,交给程序猿自行处理
    - 这是最终结果
    - 已经帮忙完成了各种参数合法/合理/兼容性的排除了!




但素!
---------------------------------

将一切合理,合适,可读的,易维护的组织为运行中的系统,
还有很多事儿要突破....


.. note:: (~_~)

    - 所以! 这就是开发的乐趣,自个儿不断的制造需求,并解决问题!
    - 这儿就不继续摆和了...

