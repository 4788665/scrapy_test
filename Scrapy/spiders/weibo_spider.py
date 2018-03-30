#!/usr/bin/env python
#coding:utf-8
# 启动命令 Scrapy crawl dmoz
from Scrapy.items import DmzjItem
from scrapy.http.request import Request
import scrapy
import io,re
import os
import Scrapy.tools.tools as tools
import Scrapy.tools.weibo_login as weibo_login

# 登陆后无法获取follow页面，会有2次302跳转，然后就到logout了，还没搞明白

g_headers = {
    'Host' : 'weibo.com',
    'Connection': 'keep-alive',
#    'cookie': 'SUB=_2A253v0rQDeRhGedM7loZ9S3OyTiIHXVUzTsYrDV_PUNbm9ANLRfdkW9NWMGebx6BuUmKU6bKvS4clCoTqOrpWMk1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5881a9EHLp7s2lCfF2PrAy5NHD95Qpeo-R1h-0eozXWs4DqcjqK2LWK.M_i--RiKn0iK.ci--fi-82iK.7; ALF=1553755648; SCF=AppGvGhCD8T_AbiPkARdYwtjfcpASrIXFca0SFz8lYoTXB2iqv0U9CKX7fIq5uyfntH9ce-cMc_kR5pro8v3Ywg.; ALC=ac%3D27%26bt%3D1522219648%26cv%3D5.0%26et%3D1553755648%26ic%3D1929352483%26scf%3D%26uid%3D1258853224%26vf%3D1%26vs%3D0%26vt%3D2%26es%3Da029a79d75f34f9d07b213d1df94f7ab; sso_info=v02m6alo5qztKWRk5ClkKOgpY6EkKWRk5SljoOYpY6EkKWRk5SlkKOkpZCjkKWRk6ClkKSQpZCkiKadlqWkj5OEso2ToLiNk4yyjKOQwA==; tgc=TGT-MTI1ODg1MzIyNA==-1522219648-yf-84D32E2862B48DB8B2AC0520D331F811-1; LT=1522219648; login=1d143a736fdf93d35dc1b24d4482f559',
    'Accept' : '*/*',
#    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
    'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding' : 'gzip, deflate, sdch, br',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.292',
}

g_cookies = []

class DmozSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["weibo.com"]
    main_page = "https://weibo.com"
    save_path = 'weibo'
    start_urls = [main_page,]
    
    def start_requests(self):
        global g_headers, g_cookies
        
        login_session = weibo_login.weibo_login('keepmemory@sina.com', '1qaz3edc')
        if login_session == None:
            print '---EXIT!!-----'
            return []
        
#        g_headers = login_session.headers
        g_cookies = login_session.cookies.get_dict()
#        g_headers['cookie'] = g_cookies
        
        print 'header=', g_headers
        return [
                Request(url = 'https://weibo.com/' + '6504059708'+'/follow', 
                        cookies = g_cookies,
                        headers = g_headers,
                        callback = self.parse)
            ]    


    def parse(self, response):
        if 1 :  # 保存页面
            filename = self.save_path + '.html'
            tools.save_to_file(filename, response.body)
            #filename = response.url.split("/")[-2] + '.html'
            #filename = self.save_path + '.html'
            #with open(filename, 'wb') as f:
            #    f.write(response.body)
        return
        
        # 提取书名、作者和简介
        if 0 :
            comic_name = response.xpath('//div[@class="UG_contents"]//h3[@class="list_title_b"]/a').extract()
            print comic_name
            self.save_path = comic_name
        
        tools_mkdir(self.save_path)

        requests = []
#        return requests
    
        
        # 提取章节名和url
        
        
        div_list = response.xpath('//div[@class="UG_contents"]//h3[@class="list_title_b"]/a')
        for index, chapter in enumerate(div_list):
            url = self.host_url + chapter.xpath('@href').extract()[0]
            name = chapter.xpath('text()').extract()[0]
            #name = tools_avalid_name(name)


            print name, url
        return requests
            
        
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
        
 
                   
def tools_mkdir(dir_path) :
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    
def tools_get_filename(file_path) :
    url_split = file_path.split("/")#[-1] + '.log'
    return url_split[-1]

def tools_avalid_name(file_path) :
    return file_path.strip().replace("\n\r", '')
    