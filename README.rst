logging-color-formatter
=======================

.. image:: https://github.com/leplatrem/logging-color-formatter/actions/workflows/test.yml/badge.svg
        :target: https://github.com/leplatrem/logging-color-formatter/actions

.. image:: https://img.shields.io/pypi/v/logging-color-formatter.svg
        :target: https://pypi.python.org/pypi/logging-color-formatter


A colored logging formatter.

Installation
------------

::

    pip install logging-color-formatter


Usage
-----

.. code-block:: ini

    [loggers]
    keys = root

    [handlers]
    keys = console

    [formatters]
    keys = generic

    [logger_root]
    level = DEBUG
    handlers = console

    [handler_console]
    class = StreamHandler
    args = (sys.stdout,)
    level = NOTSET
    formatter = generic

    [formatters]
    keys = color

    [formatter_color]
    class = logging_color_formatter.ColorFormatter


Changes
-------

See [Github Releases](https://github.com/leplatrem/logging-color-formatter/releases)


Run tests
---------

::

    py.test


Licence
-------

* Apache License v2
