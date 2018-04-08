#!/usr/bin/env python
#coding:utf-8
# 启动命令 Scrapy crawl dmoz
from Scrapy.items import DmzjItem
import Scrapy.tools.tools as tools
import scrapy
import io,re
import os

# 由于漫画网站的页面都是用js动态生成链接的，当前还不会，因此本页面功能无效



class DmozSpider(scrapy.Spider):
       
    name = "dmzj"
    allowed_domains = ["dmzj.org"]
    host_url = "https://www.dmzj.com"
    main_page = "/info/wanjiexianzong.html"
    save_path = ''
    start_urls = [host_url + '/' + main_page,]
 
    
    def parse(self, response):
        
        # 提取书名、作者和简介
        html_desc = response.xpath('//div[@class="comic_deCon"]')
        if len(html_desc) == 0 :
            print u'\n找不到图书信息，退出!!\n'
            return []
        
        comic_name = html_desc[0].xpath('//h1/a/text()').extract()[0]
        comic_artic = html_desc[0].xpath('//ul[@class="comic_deCon_liO"]/li/text()').extract()[0]
        comic_desc = html_desc[0].xpath('//p[@class="comic_deCon_d"]/text()').extract()[0]
        print comic_name
        print comic_artic
        print comic_desc
        
        self.save_path = 'download/%s' % comic_name       
        tools.create_dirs(self.save_path)

        requests = []
#        return requests
    
        
        # 提取章节名和url
        
        
        '''
        div_list = response.xpath('//ul[@class="list_con_li autoHeight"]/li/a')
        for index, chapter in enumerate(div_list):
            url = chapter.xpath('@href').extract()[0]
            chapter_name = chapter.xpath('//span[@class="list_con_zj"]/text()').extract()[0]
            chapter_name = tools.get_avalid_name(chapter_name)

            chapter_path = '%s\%s' % (comic_name, chapter_name)
            tools.create_dirs(chapter_path)
            print chapter_name, url
            return requests
            
        '''

        url = "https://www.dmzj.com/view/wanjiexianzong/71272.html"
        chapter_name = u'第31话'
        chapter_path = '%s\%s' % (comic_name, chapter_name)

        item = DmzjItem()
        item['chapter_name'] = chapter_name
        item['save_path'] = chapter_path
        request = scrapy.Request(url, callback=self.parse_chapter, dont_filter=True)
        request.meta['item'] = item
        requests.append(request)


        return requests


    def parse_chapter(self, response):
    
        tools.save_to_file(tools.get_filename(response.url), response.body)
        return
            
        item = response.meta['item']            
        
        page_lst = response.xpath('//div[@id="mainView"]//li/img[@src]')
#        print '-------', page_lst
        if len(page_lst) == 0:
            print "page_select not find!!! Exit!!!!"
            return []
        
        print page_lst
        #for page in page_lst:
         #   item['page_name'] = 
          #  chapter_content = sel.extract()
           # f.write(chapter_content + '\n\n')        
  