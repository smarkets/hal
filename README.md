hal
===

Our Jabber chat bot. Based on [Hubot](http://hubot.github.com) by GitHub but written in Python instead of CoffeeScript.

Requirements
============

* unix-compatible operating system
* make
* Python 2.x >= 2.6
 * virtualenv

Running
=======

Following environment variables are supported right now (both optional):

* ``HAL_CONFIGURATION_DIRECTORY`` - path to directory containing ``hal.cfg`` file, configuration file placed where has the highest priority
* ``HAL_PLUGIN_DIRECTORIES`` - comma-separated list of directories where bot should look for plugins

To configure `hal` you can either directly edit ``etc/hal.cfg`` or copy it somewhere else and fill using correct values.

To run it simply execute::

	make run
