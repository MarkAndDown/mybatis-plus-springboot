import os
import csv

# 定义待查找文件类型的列表
file_types = ['.java', '.sql', '.jsp', '.PLSQL']
# 定义待查找的字符串
target_str = 'PRD_18568'

# 定义查找函数
def search_files(root_path, target_str, file_types):
    # 定义结果列表
    result = []
    # 遍历根目录下的所有文件和文件夹
    for root, dirs, files in os.walk(root_path):
        # 遍历当前目录下的所有文件
        for filename in files:
            # 判断文件类型是否在待查找的文件类型列表中
            if os.path.splitext(filename)[1] in file_types:
                # 拼接文件路径
                file_path = os.path.join(root, filename)
                # 判断文件是否已经被记录
                if file_path not in result:
                    # 打开文件并读取内容
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # 判断文件内容是否包含目标字符串
                        if target_str in content:
                            # 记录结果
                            result.append(file_path)
    return result

# 定义要查找的多个文件夹路径
root_paths = ['C:/CSMS', 'D:/']

# 定义结果列表
results = []

# 遍历每个文件夹路径并查找目标文件
for root_path in root_paths:
    # 调用查找函数
    files = search_files(root_path, target_str, file_types)
    # 遍历查找结果并记录到结果列表中
    for file_path in files:
        # 判断文件是否已经被记录
        if file_path not in results:
            results.append(file_path)

# 将结果写入CSV文件
with open('search_result.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # 写入表头
    writer.writerow(['路径', '文件名'])
    # 遍历结果列表并写入CSV文件
    for file_path in results:
        writer.writerow([os.path.dirname(file_path), os.path.basename(file_path)])
