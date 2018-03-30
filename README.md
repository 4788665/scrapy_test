# scrapy_test
learn scrapy

## tsxsw ##
爬小说网站《吞噬小说网》下的小说章节，每次只能爬一本小说，命令格式如下：<br>
Scrapy crawl tsxsw -a url="http://www.tsxsw.com/html/44/44043/"
其中url是小说目录页的地址

并发抓取，每一章节生成一个文件，然后利用dos命令进行合并，例如：<br>
copy download\和表姐同居的日子\* download\和表姐同居的日子.txt

## dmoz ##
功能未完成，因为页面中的java不会解析

## weibo ##
功能未完成，因为登陆以后读取follow页面时，有多次302跳转。。。。。。

