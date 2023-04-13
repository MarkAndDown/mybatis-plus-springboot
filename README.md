# mybatis-plus-springboot
mybatis-plus集成springboot生成VO版本的增删改查和分页查询

import os
import csv

path = "C://CSMS" # 指定路径
suffixes = [".java", ".sql", ".jsp"] # 指定后缀名
target_str = "PRD_18568" # 指定要搜索的字符串

result = set() # 存储搜索结果的集合

def search_file(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(tuple(suffixes)): # 只查找指定后缀名的文件
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    if target_str in content: # 如果文件内容包含指定字符串，则将路径和文件名添加到结果集合中
                        result.add(os.path.join(root, file))

search_file(path)

with open("result.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["路径", "文件名"])
    for file in result:
        writer.writerow([os.path.dirname(file), os.path.basename(file)])
