# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    chapter_name = scrapy.Field()
    chapter_content = scrapy.Field()
    curr_url = scrapy.Field()
    next_url = scrapy.Field()
    index = scrapy.Field()

class DmzjItem(scrapy.Item):
    chapter_name = scrapy.Field()
    save_path = scrapy.Field()
    page_name = scrapy.Field()
    

from scrapy.exceptions import DropItem
    
class ScrapyPipeline(object):

    # put all words in lowercase
    words_to_filter = ['politics', 'religion']

    def process_item(self, item, spider):
        print item
        #for word in self.words_to_filter:
        #    if word in unicode(item['description']).lower():
        #        raise DropItem("Contains forbidden word: %s" % word)
        #else:
        return item
