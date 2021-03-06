#!/usr/bin/env python
#coding:utf-8
# 启动命令 Scrapy crawl tsxsw
from Scrapy.items import ScrapyItem
from txt_spider import TxtSpiderBase
import Scrapy.tools.tools as tools
import scrapy
import io
import os

# 爬小说网站
# 如果用目录页作为startpage，则解析目录页以后产生的多个request，是并发的进行请求，会导致保存的小说章节错序，因此，抓小说的时候，用第一张的页面作为起始页
# 并发抓取，每一章节生成一个文件，然后只用dos命令进行合并，例如
# copy download\和表姐同居的日子\* download\和表姐同居的日子.txt

class TsxswSpider(TxtSpiderBase):
    name = "tsxsw"
    allowed_domains = ["tsxsw.com"]
    main_page = "http://www.tsxsw.com/html/44/44043/"
    start_urls = [main_page,]
#    rules = [Rule(LinkExtractor(allow=['/tor/\d+']), 'parse_torrent')]   

    def __init__(self, url=None, *args, **kwargs):
        super(TsxswSpider, self).__init__(*args, **kwargs)
        if url is not None:
            self.main_page = url
            self.start_urls = [url]

    
    def parse(self, response):
        
        # 提取书名、作者和简介
        div_articleinfo = response.xpath('//div[@class="articleinfo"]')[0]
        div_article = div_articleinfo.xpath('//div[@class="p1"]')
        div_comment = div_articleinfo.xpath('//p[@class="p3"]')

        # 作者和简介有可能为空，因此多一次处理
        book = div_article[0].xpath('//h1/text()').extract()[0]
        article = div_article[0].xpath('//span/text()').extract()
        article = '' if len(article) == 0 else article[0]
        comment = div_comment[0].xpath('text()').extract()
        comment = '' if len(comment) == 0 else comment[0]
        
        self.book_name(book)
        
        # 写简介
        content = u'书名:%s\n%s\n简介:\n%s\n' % (book, article, comment)
        self.write_content(0, book, content)
        
        print book, article
        print comment
        
        requests = []
#        return requests
    
        
        # 提取章节名和url
        div_list = response.xpath('//div[@class="chapterlist"]/ul/li/a')
        for index, chapter in enumerate(div_list):
            url = self.main_page + chapter.xpath('@href').extract()[0]
            name = chapter.xpath('text()').extract()[0]
            name = tools.get_avalid_name(name)
            #print name, url
                    
            item = ScrapyItem()
            item['index'] = index + 1
            item['chapter_name'] = name
            request = scrapy.Request(url, callback=self.parse_chapter, dont_filter=True)
            request.meta['item'] = item
            requests.append(request)
            
        self.chapter_count(len(requests))

        return requests

    def parse_chapter(self, response):
        
        item = response.meta['item']
        
        div_main = response.xpath('//div[@class="main w chapter"]')
        if len(div_main) == 0:
            print "main w chapter not find!!! Exit!!!!"
            return []
        
        
        # 取标题和内容
        #div_title = div_main[0].xpath('h1/text()') #标题使用传入的参数
        div_content = div_main[0].xpath('div[@id=\'content\']/p/text()')
        if len(div_content) == 0:
            print "title or content not find!!! Exit!!!!"
            return []
        
        #chapter_name = div_title[0].extract()
        chapter_name = item['chapter_name']
        content_lst = [ chapter_name ]
        for sel in div_content:
            content_lst.append( sel.extract() )
            
        self.write_content(item['index'], chapter_name, content_lst)

        self.together_book()

