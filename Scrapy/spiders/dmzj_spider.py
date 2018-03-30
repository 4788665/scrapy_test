#!/usr/bin/env python
#coding:utf-8
# 启动命令 Scrapy crawl dmoz
from Scrapy.items import DmzjItem
import scrapy
import io,re
import os

# 由于漫画网站的页面都是用js动态生成链接的，当前还不会，因此本页面功能无效



class DmozSpider(scrapy.Spider):
    '''
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

    '''            
    name = "dmzj"
    allowed_domains = ["dmzj.org"]
    host_url = "http://ac.qq.com"
    main_page = "Comic/comicInfo/id/552724"
    save_path = '2'
    start_urls = [host_url + '/' + main_page,]
 
    
    def parse(self, response):
        
        # 提取书名、作者和简介
        comic_name = response.xpath('//h2[@class="works-intro-title ui-left"]/strong/text()').extract()[0]
        print comic_name
        self.save_path = comic_name
        
        tools_mkdir(self.save_path)

        requests = []
#        return requests
    
        
        # 提取章节名和url
        
        '''
        div_list = response.xpath('//ol[@class="chapter-page-all works-chapter-list"]//a')
        for index, chapter in enumerate(div_list):
            url = self.host_url + chapter.xpath('@href').extract()[0]
            name = chapter.xpath('text()').extract()[0]
            name = tools_avalid_name(name)

            chapter_path = '%s\%03d_%s' % (comic_name, index+1, name)
            tools_mkdir(chapter_path)
            print name, chapter_path
            return requests
            
        '''
        chapter_path = u'猫妖的诱惑\001_我可以吻你吗？'
        name = u'我可以吻你吗？'
        url = "http://ac.qq.com/ComicView/index/id/552724/cid/1"

        item = DmzjItem()
        item['chapter_name'] = name
        item['save_path'] = chapter_path
        request = scrapy.Request(url, callback=self.parse_chapter, dont_filter=True)
        request.meta['item'] = item
        requests.append(request)


        return requests


    def parse_chapter(self, response):
    
        filename = tools_get_filename(response.url)
        with open(filename, 'wb') as f:
            f.write(response.body)
            
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
        
 
# 检查目录是否存在，如果不存在，则创建，只支持最后一级目录不存在
def tools_mkdir(dir_path) :
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    
# 从路径中取出文件名（最后一个/后边的部分)
def tools_get_filename(file_path) :
    url_split = file_path.split("/")#[-1] + '.log'
    return url_split[-1]

# 删除字符串中的回车换行符和空格
def tools_avalid_name(file_path) :
    return file_path.strip().replace("\n\r ", '')
    