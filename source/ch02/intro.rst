.. include:: ../LINKS.rst


好了,已经完成了预期的 :

- 用起 `SAE`_ 
- 包装 `金山网址云安全开放API <http://code.ijinshan.com/api/devmore4.html#md1>`_ 为 `REST`_ 服务
- 只要 `curl -d "uri=http://sina.com" urisaok.sinaapp.com/chk/` 即可返回,金山云的数据!


.. sidebar:: 推荐
    :subtitle: `agentzh <http://agentzh.org/>`_ 妙吼

    - `命名的艺术 <http://agentzh.org/misc/slides/naming/#2>`_
    - `“命名”课回顾 <http://agentzh.org/misc/slides/naming/naming_recap.html#2>`_

    

**但是** :

- 代码很集中,业务逻辑离头部很远,很难看
- 当没有进行 `POST` 请求时,以及各种其它意外请求时,并没智能的捕获,并提示
- 变量名设计的都很挫,需要重构
...

最最最要命的是:

    - 每次来的查询请求都要访问 金山云 完成查询
    - 即使,多数情况里,大家总是反复对常见的疑似钓鱼网站进行安全查询的吼,,,
    

所以,继续折腾...

