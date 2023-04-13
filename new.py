import os
import csv

# 指定要查找的路径
paths = ["C:/CSMS", "D:/", "E:/"]

# 指定要查找的文件后缀名
suffixes = [".java", ".sql", ".jsp", ".PLSQL"]

# 指定要查找的字符串
target_str = "PRD_18661"

# 用于存储文件名和文件路径的列表
file_list = []

# 递归查找符合要求的文件
for path in paths:
    for root, dirs, files in os.walk(path):
        for filename in files:
            # 只查找指定后缀名的文件
            if filename.endswith(tuple(suffixes)):
                file_path = os.path.join(root, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                    # 如果文件内容包含目标字符串，则将文件路径和文件名添加到列表中
                    if target_str in file_content:
                        file_list.append((filename, file_path))

# 去重
file_list = list(set(file_list))

# 按照后缀名排序
file_list.sort(key=lambda x: suffixes.index(os.path.splitext(x[0])[1]))

# 将结果写入 csv 文件
with open("result.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["File Name", "File Path"])
    for file_info in file_list:
        writer.writerow(file_info)
