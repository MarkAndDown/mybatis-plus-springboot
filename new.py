import os
import csv

# 定义要查找的文件后缀
extensions = ['.java', '.sql', '.jsp', '.PLSQL']

# 定义要查找的字符串
search_string = 'PRD_18661'

# 定义要搜索的文件夹路径
search_paths = ['C:/CSMS', 'D:/', 'E:/']

# 保存搜索结果的列表
result = []

# 遍历所有路径
for path in search_paths:
    # 遍历所有文件和文件夹
    for root, dirs, files in os.walk(path):
        # 遍历所有文件
        for file in files:
            # 获取文件后缀
            extension = os.path.splitext(file)[1]
            # 如果文件后缀符合要求
            if extension in extensions:
                # 拼接文件路径
                file_path = os.path.join(root, file)
                # 查找文件中是否含有指定字符串
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    contents = f.read()
                    if search_string in contents:
                        # 将结果加入列表中
                        result.append((os.path.abspath(file_path), os.path.abspath(root)))
                        
# 去除重复项
result = list(set(result))

# 将结果保存到CSV文件中
with open('result.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Filename', 'Path'])
    writer.writerows(result)
