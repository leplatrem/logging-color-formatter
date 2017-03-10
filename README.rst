logging-color-formatter
=======================

.. image:: https://img.shields.io/pypi/v/logging-color-formatter.svg
    :target: https://pypi.python.org/pypi/logging-color-formatter
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/leplatrem/logging-color-formatter.png
   :target: https://travis-ci.org/leplatrem/logging-color-formatter
   :alt: Latest Travis CI build status

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


Licence
-------

* Apache License v2
