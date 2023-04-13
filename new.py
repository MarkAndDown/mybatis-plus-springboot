import os
import csv

file_exts = ['.java', '.sql', '.jsp', '.PLSQL']  # 需要搜索的文件后缀
search_str = 'PRD_18661'  # 需要搜索的字符串
search_dirs = ['C:/CSMS/back', 'D:', 'E:']  # 需要搜索的目录

result = set()

for search_dir in search_dirs:
    for root, dirs, files in os.walk(search_dir):
        for filename in files:
            file_ext = os.path.splitext(filename)[1]
            if file_ext in file_exts:
                filepath = os.path.join(root, filename)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if search_str in content:
                        result.add((filename, filepath))

# 将结果按照文件后缀排序
result = sorted(result, key=lambda x: file_exts.index(os.path.splitext(x[0])[1]))

# 将结果写入CSV文件
with open('result.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['文件名', '文件路径'])
    for item in result:
        writer.writerow(item)
