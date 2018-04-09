# scrapy_test
learn scrapy

# History #
**2018/4/9** 增加奇书网小说爬取



## 小说 ##

- [吞噬小说网](http://www.tsxsw.com) <br>

 `Scrapy crawl tsxsw -a url="http://www.tsxsw.com/html/44/44043/"`

> 并发抓取，每一章节生成一个文件，然后利用dos命令进行合并，例如：<br>
> copy download\和表姐同居的日子\* download\和表姐同居的日子.txt


- [奇书网](http://www.qisuu.la) <br>
  `scrapy crawl qisuu -a url=https://www.qisuu.la/du/36/36889/`


## dmoz ##
功能未完成，因为页面中的java不会解析


## weibo ##
功能未完成，因为登陆以后读取follow页面时，有多次302跳转。。。。。。

