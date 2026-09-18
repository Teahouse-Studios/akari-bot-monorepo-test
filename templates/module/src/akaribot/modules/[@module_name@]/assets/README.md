包内只读静态资源目录
====================

放置随包分发的只读资源，例如词表、字体、映射表、图标。运行时下载或用户可写的
文件不放这里，它们属于实例目录（`package_data()`，见 T3.1）。

读取方式：

.. code-block:: python

    from importlib.resources import files

    data = (files("akaribot.modules.[@module_name@]") / "assets" / "words.txt").read_text(encoding="utf-8")

不要用 `Path(__file__).parent` 定位包内资源：安装为 wheel 之后该路径不成立。
