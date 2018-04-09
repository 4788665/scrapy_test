#!/usr/bin/env python
#coding:utf-8

import scrapy
import os,sys,io
import Scrapy.tools.tools as tools


class TxtSpiderBase(scrapy.Spider):
	root_path = os.getcwd() + '/download'
	save_path = ''
	book_name = ''
	chapter_remain = 0

	# 设置/返回 剩余的章节数量
	def chapter_count(self, count=None) :
		if count != None:
			self.chapter_remain = count
		return self.chapter_remain

	# 设置/返回 剩余的图书名称
	def book_name(self, book=None) :
		if book != None:
			self.book_name = book
			self.save_path = self.root_path + '/' + self.book_name
			tools.create_dirs(self.save_path)
		return self.book_name
		
	def save_response(self, repsonse):
		file_name = '%s/%s' % (os.getcwd(), tools.get_filename(response.url) )
		tools.save_to_file(file_name, response.body)
			
	# 写文件
	def write_content(self, idx, name, content):
		# 写简介
		file_name = '%s/%04d_%s.txt' % (self.save_path, idx, name)
		f = io.open(file_name, 'w', encoding='utf-8')
		
		if isinstance(content, str) or isinstance(content, unicode):
			f.write(content + '\n')
		
		elif isinstance(content, list) :
			for i in content:
				f.write(i + '\n')
		
		f.close()		
	
	def together_book(self) :
		self.chapter_remain -= 1
		
		# 取得全部章节以后，用shell命令进行拼接成单一文件        
		if self.chapter_remain != 0 :
			return
		
		cmd = 'copy %s/* %s/%s.txt' % (self.save_path, self.root_path,  self.book_name)
		if tools.is_windows_os() :
			cmd = cmd.replace('/', '\\')
		cmd = cmd.encode("GBK", 'ignore');
		os.system(cmd)
			