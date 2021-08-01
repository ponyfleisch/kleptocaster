Kleptocaster
============

Generates a simple rss file from a directory of media files.

Installation
------------

From github::

    pip install git+https://github.com/ponyfleisch/kleptocaster


Using Kleptocaster
------------------

Usage::

    kleptocaster \
        --directory ~/Documents/cast \
        --baseurl http://my.custom.domain/kleptocast/ \
        --image cast.jpg \
        --descr "Media files of dubious and/or unknown origin." \
        --title "Kleptocast"

The image file is expected to be in the media files directory. By default, this will generate a file named feed.xml in the media directory, you can change the filename using the ``--output`` option.

Only mp3, mp4 and aac files are included by default, use the ``--extensions`` option to change this, e.g. ``--extensions mp3,mp3``.

Note that this is not streaming the output and as such might consume a lot of memory or fail when used with a large directory.