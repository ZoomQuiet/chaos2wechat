.. include:: ../LINKS.rst


FSM
==============

注意!

- `FSM`_ 不是: 飞天面条神教(Flying Spaghetti Monsterism)
- `FSM`_ 不是: 自由软件运动(Free software movement)
- `FSM`_ 而是: `有限状态机`_ (Finite State Machine)

简单的说:

- `有限状态机`_ 称有限状态自动机，简称状态机，是种算法思想
- 是表示有限个状态以及在这些状态之间的转移和动作等行为的数学模型。
- 一般 `有限状态机`_ 由一组状态、一个初始状态、输入和根据输入及现有状态转换为下一个状态的转换函数组成


提示
---------------------------------

是神奇的列表小伙伴提示的, 曰:"

- 这就是工作流中的 `有限状态机`_ 情景
- 一系列有限度的,有明确顺序的状态
- 状态间的切换,也是明确的不变的条件
- 这种情况,使用 `FSM`_ 来解决就对了!

"


方案
---------------------------------

通过可爱的 `Google`_ 可以快速查询到各种Python 相关的 `FSM`_ 支持模块,比如:

- `Finite State Machines in Python – No Pity for the Masses <http://www.seethroughskin.com/blog/?p=793>`_
- `python - Code Golf: Finite-state machine! - Stack Overflow <http://stackoverflow.com/questions/4661818/code-golf-finite-state-machine>`_
- `fsm - What are the best Python Finite State Machine implementations - Stack Overflow <http://stackoverflow.com/questions/5492980/what-are-the-best-python-finite-state-machine-implementations>`_
- `FiniteStateMachine - Python Wiki <https://wiki.python.org/moin/FiniteStateMachine>`_
    - `AT&T's Weighted FSM in python <http://www2.research.att.com/~fsmtools/fsm/man4/fsmpy.html>`_
    - `FSME <http://fsme.sourceforge.net/>`_ , A graphical FSM Editor w/ python target
    - `FSA <http://osteele.com/software/python/fsa/>`_
    - `fsmpy module <http://www.research.att.com/projects/mohri/fsm/doc4/fsmpy.html>`_
    - `fsm.py <http://www.smontanaro.net/python/fsm.py>`_ , Skip Montanero's FSM
    - `fysom <https://github.com/oxplot/fysom>`_ ,A slick FSM implementation that provides function callbacks for each state.

等等....

但是! 并不是每一个都好用的!

- 有的虽然很著名,比如 `fysom <https://github.com/oxplot/fysom>`_  是从 JavaScrip 的成功模块转换来的,甚至于有很多语言的实现! 但是,这是基于 网页富应用的情景,用户在网页不断的交互,状态的转变在客户端连续进行的,不吻合我们的离散性请求场合!
- 有的是用来绘制 `有限状态机`_ 图谱的!
- 有的看起来高端大气上档次,可是,就是无法快速从示例中理解要怎么应用!

于是,动用在 `github`_ 中锻炼出来的同类模块选择方式:

1. 看官方网站是否可访问
2. 看官方文档是否完备
3. 尝试在一刻钟之内,是否可以根据文档+示例,完成一个小实例!





pyfsm
^^^^^^^^^^^^^^^^^^^^^^

`pyfsm`_ - Pure Python Implementation of a Finite State Machine 

胜出!!

::

    @state('hello_world') # task 'hello_world'
    @transition(1, 'goodbye') # transitions on 1 to the goodbye state
    def say_hello(tsk): # state name is say_hello, the task is the second object
        ...


这是唯一一个利用Python 修饰器特性来实现 `FSM`_ 的模块,是 `Pythonic`_ 的!-)

``samples.py`` 十分简洁以及明快:

.. literalinclude:: samples.py
    :language: python


目测跟 `Bottle`_ 的使用非常相近! `有限状态机`_ 的使用过程如下:

1. ``import pyfsm`` 先导入模块, 因为整个模块和 `Bottle`_ 一样,就一个文件,所以,不用安装到系统目录,只要包含在网站目录中,可以引用的到就好!
2. ``pyfsm.Registry.get_task('say_hello')`` 来生成一个 `有限状态机`_
3. ``say_hello.start('meet_and_greet')`` 来初始化当然 `有限状态机`_ 的起始状态
4. ``say_hello.send('hi')`` 就是向 `有限状态机`_ 发送指令, 由 `有限状态机`_ 自个儿进行合理判定,是否响应,或是是否状态跳转


而同具体执行的函式进行绑定的形式也非常的 `Pythonic`_:

::

    from pyfsm import state, transition
    ...

    @state('say_hello')
    @transition('goodbye', 'goodbye')
    def meet_and_greet(self):
        ...

    @state('say_hello')
    def goodbye(self):
        ...


简单的说:

1. ``@state('say_hello')`` 标明当前函式从属哪个 `有限状态机`_
2. ``@transition('goodbye', 'goodbye')`` 绑定当前状态的迁移条件,以及目标状态
3. ``def goodbye(self):`` 就是匹配目标状态的响应函式


经过探索, 发现 `pyfsm`_ 不仅仅支持状态回调,
而且, 也支持条件的堆叠判定迁移.

这样一来,



.. _fig_3_2:
.. figure:: ../_static/figs/chaos3-2-gdg_seek_words.png

   插图 3-2 如果包含一个支持随时退出流程的 ``*`` 指令


所设计的 `有限状态机`_ 对应的可执行代码就是类似::

    @state('weknow')
    @transition('s', 'seek')
    def setup(self):
        print "start->"

    @state('weknow')
    @transition('dd', 'papers')
    ...
    @transition('ot', 'papers')
    @transition('*', 'end')
    def seek(self):
        print "start->seek->"

    @state('weknow')
    @transition('no', 'no_paper')
    @transition('*', 'end')
    def papers(self):
        print "start->seek->papers"

    @state('weknow')
    @transition('end', 'end')
    @transition('*', 'end')
    def number_paper(self):
        print "start->seek->papers->paper"

    @state('weknow')
    def end(self):
        print "->end"


而对应的原先一大堆的 ``if elif else`` 判定树就可以全部丢掉了!
变成类似的非常简单的:


.. code-block:: python
    :linenos:
    :emphasize-lines: 12-14

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
            weknow = pyfsm.Registry.get_task('weknow')
            weknow.start("当前用户上次状态")
            return weknow.send(__Content)


即!

- 将复杂的有前后顺序要求的流程上下文判定,都丢给 `有限状态机`_ 去处理!
- 具体调运哪个函式, 通过 ``@transition()`` 去声明就好, 只要注意,迁移条件字串和状态执行函式名的区别
- 唯一的问题是 ``当前用户上次状态`` 缓存到哪儿,以便 `有限状态机`_ 获得,并完成当前交互的起始状态初始化?


但素!
---------------------------------

还有, 每次要从标准的 ``request`` 对象中逐一提取需要的字串,然后通过 Python 的内置简单字串模板来替换成合理的 公众号要求的 `XML`_ 太不优雅了!!!

代码也看起来很不简洁! 肿么办?!

是时候使用合适的封装支持模块了! 心里一定有个声音在大声吼...

经过快速对比:

- `twinsant/pyweixin <https://github.com/twinsant/pyweixin>`_ 是好看薄/云彩直播的 `蚂蚁 <http://www.haokanbu.com/user/1/>`_ 的作品, 也是单纯的字串模板替换
- `jeffkit/wechat`_ 则是珠三角技术沙龙的 `Jeff <http://www.jeffkit.info/about/>`_ 的, 这位创业程序猿不但iOS/Android 跨平台代码写的好,而且玩的一手好 Ukulele ,骗得一位漂亮老婆,也是一名光荣的奶爸! 而且!关键加分是:
    - `gztechparty/techparty <https://github.com/gztechparty/techparty>`_ 是应用此模块完成的 珠三角技术沙龙公众号应答平台的代码!
    - 有真实在用的代码可以参考!

果断用 `jeffkit/wechat`_  了!

据作者本人吹嘘,使用?那叫个简单! 兼容?那叫个全面!

- 但素! 文档是一大波浓浓的 `Django`_ 味儿!
- 完全没说其它框架怎么简单使用的,,,
- 幸好其核心也就一个文件 `official.py <https://github.com/jeffkit/wechat/blob/master/wechat/official.py>`_ 
- 幸好也提供了各种 demo : `wechat/demo at master · jeffkit/wechat <https://github.com/jeffkit/wechat/tree/master/demo>`_


得以明白了关键的调用形式::

    from wechat.official import WxApplication, WxRequest, WxTextResponse, WxNewsResponse, WxArticle

    wxreq = WxRequest(request数据体) #完成初始化
    ...
    WxTextResponse(想返回的文本, wxreq).as_xml() #返回文本格式的XML
    ...
    p1 = WxArticle(标题,Url=文章链接,PicUrl=图片链接) # 生成图文文章信息
    p2 = WxArticle(标题,Url=文章链接,PicUrl=图片链接)
    WxNewsResponse([p1, p2]], wxreq).as_xml() #返回多图文 文章格式XML


的确比原先的形式::

    xml = etree.XML(request.forms.keys()[0])
    fromUser = xml.findtext("ToUserName")
    toUser = xml.findtext("FromUserName")
    __MsgType = xml.findtext("MsgType")
    __Content = xml.findtext("Content")

    ...
            return CFG.TPL_TEXT% locals()


要有范儿,也 `Pythonic`_ 的多了!


贯通所有!
---------------------------------

清点一下现在已经探索完成的所有因素:

1. `Bottle`_ 以明快的形式,将 wechat 来的消息得以合理的截收以及处理,形式::

    @APP.post('/echo')
    def wechat_post():
        print request.forms.keys()[0]
        ...

2. `pyfsm`_ 以 `Pythonic`_ 的形式,将 `FSM`_ 的状态/条件自然的绑定到一批自然函式上,可以完成复杂的 `有限状态机`_ 快速描述
3. `jeffkit/wechat`_ 的公众号封装,以简洁的形式完成了麻烦的 `XML`_ 拼装/兼容工作

目前的阻碍只有:

1. 如何记忆上次成员的 `FSM`_ 状态以便再次初始化?
2. 如何在 `pyfsm`_ 中传递 `jeffkit/wechat`_ 的 ``wxreq`` 对象?


记忆历史状态
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
在 `SAE`_ 端,快速缓存字串?! ~ 不就是 `KVDB` 嘛!

- 在对应的成员节点中,追加一个 ``fsm`` 字段保存不就好了?!
- 每当提交了合法的指令,引发 `有限状态机`_ 的状态变迁,就再次替换缓存新的状态字串呗!

那么核心响应函式就应该形如:





.. code-block:: python
    :linenos:
    :emphasize-lines: 2,5,8-9,11-14

    @APP.post('/echo')
    def wechat_post():
        wxreq = WxRequest(request.forms.keys()[0])
        uid = hashlib.sha1(toUser).hexdigest()
        G_CRT_USR = KV.get(uid)
        wxreq.crt_usr = G_CRT_USR
        # usage pyfsm as FSM echo all kinds of usr ask
        weknow = pyfsm.Registry.get_task('weknow')
        if G_CRT_USR['fsm']:
            weknow.start2(G_CRT_USR['fsm'], wxreq)
        else:
            G_CRT_USR['fsm'] = "setup"
            __update_usr(G_CRT_USR)
            weknow.start2('setup', wxreq)
        return weknow.send2(wxreq.Content.strip(), wxreq)


其中:

- ``wxreq.crt_usr = G_CRT_USR`` 是通过查阅代码,发现 `jeffkit/wechat`_ 中 ``WxRequest`` 的实例其实是可以追加任意类变量的, 所以,干脆将总是需要四处使用的当前用户数据对象,统一追加到其中,方便传递进其它函式使用!
- ``weknow.start2('setup', wxreq)`` 纯粹就是对 `pyfsm`_ 的增订设想
    - 只需要原先的初始化( ``start`` )或是触发( ``send`` )函式可以接受一个新的参数
    - 就可以完成必要的数据传递, 从 `Bottle`_ 的网络请求响应函式,安全的跳到 `FSM`_ 处理函式中

怎么当前必须的增补呢?


传递请求对象
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

观察 `pyfsm`_ 的修订记录:

- `Changes - pyfsm - Pure Python Implementation of a Finite State Machine - Google Project Hosting <http://code.google.com/p/pyfsm/source/list>`_
- 可以看到,作者认为必要的功能已经完美, 在两年前就停止了修订
- 所以,吼作者是不现实的, 人家也未必有空为俺的奇怪需求进行修订
- 但是,代码在手,乍玩有我!

于是!

.. code-block:: diff
    :linenos:

    --- 3party/pyfsm.py 2013-09-26 17:34:56.000000000 +0800
    +++ ../_3party/pyfsm/pyfsm.py   2013-09-24 09:24:26.000000000 +0800
    @@ -266,60 +266,6 @@
             if trans:
                 self.start(trans)

    -    def start2(self, name, obj):
    -        """
    -        Starts the task with the given state name.
    -
    -        @param name: state name.
    -        @param obj: data obj. for func.
    -        @type name: C{str}
    -        """
    -        for x in self.exit:
    -            x(self, obj)
    -
    -        self.current_state = self.states[name]
    -        self.callbacks = {}
    -        self.exit = []
    -        self._locals = {}
    -        return self.current_state.enter2(self, obj)
    -
    -    def send2(self, event, obj):
    -        """
    -        Sends an event to this task.
    -
    -        It determines what key to use to identify the event by
    -        calling the appropriate getattr function.
    -
    -        If any callbacks are registered for this event, then they are
    -        invoked first.
    -
    -        If any transitions are registered for this event, a state transition
    -        is invoked after completing the callbacks.
    -
    -        @param event: event to send to the state machine
    -        @param obj: data obj. for func.
    -        """
    -        assert self.current_state, 'state machine is not running'
    -
    -        # recover the key for this event
    -        for getattr in (self.getattr, Registry.getattr, lambda x: x):
    -            try: key = getattr(event)
    -            except: pass
    -            else: break
    -
    -        # check callbacks first
    -        callback = self.callbacks.get(key, [])
    -        for x in callback:
    -            x(event, obj)
    -
    -        # if a transition exists, change the state
    -        trans = self.current_state.transitions.get(key, None)
    -        if trans:
    -            return self.start2(trans ,obj)
    -        else:
    -            # when state transited, call old  current_state func again!
    -            return self.current_state.enter2(self, obj)
    -
         def add_state(self, name, state):
             """
             Adds a state to this task.
    @@ -417,13 +363,11 @@
         def __init__(self, name):
             self.task = Registry.get_task(name)
             self.transitions = {}
    -
         def __call__(self, func):
             self.func = func
             self.transitions.update(getattr(func, 'transitions', {}))
             self.task.add_state(func.__name__, self)
             return self
    -
         def enter(self, task):
             """
             Entrance function to this state.
    @@ -432,15 +376,3 @@
             @type task: L{pyfsm.task}
             """
             return self.func(task)
    -
    -    def enter2(self, task, obj):
    -        """
    -        Entrance function to this state.
    -
    -        @param task: task this state is contained within
    -        @param obj: data obj. for func.
    -        @type task: L{pyfsm.task}
    -        """
    -        return self.func(task, obj)
    -

简单的复制关键函式为 ``**2`` 为名,追加一个参数,并原样返回就好!




.. note:: (~_~)

    - 所以! 这就是 ``不折腾要死星人`` 的感脚! 不断的制造问题,并解决!

