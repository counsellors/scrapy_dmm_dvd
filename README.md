scrapy_dmm_dvd - A Scrapy Crawler
[ ![Travis CI Status](https://travis-ci.org/counsellors/scrapy_dmm_dvd.svg?branch=master)](https://travis-ci.org/counsellors/scrapy_dmm_dvd)  
=========================
To crawl books,musics,dvd and others from dmm, based on scrapy framework and mongodb.

Requirements
------------

* ubuntu 14.04+
* python
* pip
* scrapy
* mongodb

That's all. It's base package of python environment!


Quick Start
------------
```
git clone git@github.com:counsellors/scrapy_dmm_dvd.git
cd scrapy_dmm_dvd/dmm_joke
scrapy crawl dvd_spider
```

Test
------------

local html crawl test

cp dmm_joke/tmp/index.html /tmp/

set start_urls to "file:///tmp/index.html" in dvd_spider.py


To Do List
----------

- <s>add mongodb</s>
- <s>find all details url in some pageb</s>
- <s>duplicate urlb</s>
- add proxy pool or via tor
- save image by pipeline
- distributed system
- support js
