import os
import csv

# 多个文件夹路径
paths = ['C:/CSMS', 'D:/', 'E:/']
# 指定后缀名
extensions = ['.java', '.sql', '.jsp', '.PLSQL']
# 指定查找的字符串
search_str = 'PRD_18661'

# 存储结果的列表
result = []

# 递归查找函数
def search_files(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            search_files(file_path)
        elif os.path.isfile(file_path) and any(file_path.endswith(ext) for ext in extensions):
            with open(file_path, 'r', encoding='utf-8') as f:
                if search_str in f.read():
                    # 去重
                    if file_path not in result:
                        result.append(file_path)

# 遍历路径列表
for path in paths:
    search_files(path)

# 根据文件类型排序
result.sort(key=lambda x: os.path.splitext(x)[1])

# 写入 csv 文件
with open('result.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['文件路径', '文件名'])
    for file_path in result:
        writer.writerow([os.path.dirname(file_path), os.path.basename(file_path)])
