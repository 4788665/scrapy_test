#!D:\5.Python\python.exe
#coding:utf-8

import io
import os

# 保存到文件中
def save_to_file(filename, string):
    with open(filename, 'wb') as f:
        f.write(string)
    f.close()
        

# 检查目录是否存在，如果不存在，则创建，只支持最后一级目录不存在
def tools_mkdir(dir_path) :
    print dir_path, os.curdir
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
# 从路径中取出文件名（最后一个/后边的部分)
def tools_get_filename(file_path) :
    url_split = file_path.split("/")#[-1] + '.log'
    return url_split[-1]

# 删除字符串中的回车换行符和空格, 在str中查找str1中的每个字符，并替换成str2
def tools_avalid_name(str, str1='\n|\r|*', str2='') :
    splits = str1.split('|')
    for x in splits:
        str = str.replace(x, str2)
    return str
    #return str.strip().replace(str1, str2)

