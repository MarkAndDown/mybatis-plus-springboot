import os
import csv

# 定义要查找的路径
paths = ["C:/CSMS/back/fd/dss/f", "D:/", "E:/"]

# 定义要查找的文件类型和要查找的字符串
extensions = ['.java', '.sql', '.jsp', '.PLSQL']
search_str = "PRD_18661"

# 定义要输出的csv文件名和列名
csv_filename = "output.csv"
csv_columns = ['序号', '展示', '文件名', '文件路径', 'Danny', 'IFP_23_RL02_PRD_18861']

# 初始化结果列表
result = []

# 递归函数查找指定文件类型的文件并判断是否包含指定字符串
def find_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            # 只处理指定后缀名的文件
            if file.endswith(tuple(extensions)):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    # 判断文件内容是否包含指定字符串
                    if search_str in f.read():
                        # 获取文件的完整路径和文件名
                        full_path = os.path.join(root, file)
                        filename = os.path.basename(full_path)
                        # 获取文件路径中去掉SourceTree之前的部分
                        path_parts = full_path.split("\\")
                        idx = path_parts.index("SourceTree")
                        file_path = "\\".join(path_parts[idx+1:])
                        # 判断文件类型，确定展示类型
                        if file.endswith('.java') or file.endswith('.jsp'):
                            display_type = 'CSMS'
                        else:
                            display_type = 'CIS'
                        # 添加结果到结果列表中
                        result.append([len(result)+1, display_type, filename, file_path, 'Danny', 'IFP_23_RL02_PRD_18861'])

# 遍历所有路径
for path in paths:
    find_files(path)

# 去重
result = list(set(tuple(row) for row in result))

# 按照文件类型排序
result.sort(key=lambda x: extensions.index(os.path.splitext(x[2])[1]))

# 写入csv文件
with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(csv_columns)
    for row in result:
        writer.writerow(row)
