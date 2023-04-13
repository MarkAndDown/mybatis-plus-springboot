import os
import csv

# 定义需要查找的路径
paths = ["C:/CSMS/back/fd/dss/f", "D:/", "E:/"]

# 定义需要查找的文件后缀和关键字
file_exts = ['.java', '.sql', '.jsp', '.PLSQL']
search_str = 'PRD_18661'

# 定义需要输出的文件名
output_filename = 'output.csv'

# 定义需要输出的列名
fieldnames = ['Index', 'Project', 'Filename', 'Path', 'Author', 'Keyword']

# 定义用于去重的集合
unique_files = set()

# 定义计数器
count = 0

# 定义项目名称字典
project_dict = {
    '.java': 'CSMS',
    '.jsp': 'CSMS',
    '.sql': 'CIS',
    '.PLSQL': 'CIS'
}

# 定义路径中需要删除的部分
path_to_remove = 'SourceTree'

# 定义作者名
author_name = 'Danny'

# 定义关键字
keyword = 'IFP_23_RL02_PRD_18861'

# 定义输出文件的打开方式
with open(output_filename, mode='w', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()

    for path in paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if any(file.endswith(ext) for ext in file_exts):
                    file_path = os.path.join(root, file)
                    if search_str in open(file_path, encoding="utf8").read():
                        # 获取文件名和后缀
                        filename, ext = os.path.splitext(file)
                        # 获取项目名称
                        project = project_dict.get(ext, '')
                        # 去除路径中的部分
                        path = root.split(path_to_remove, 1)[-1]
                        # 如果路径已存在则跳过
                        if (filename, path) in unique_files:
                            continue
                        else:
                            unique_files.add((filename, path))
                        # 写入csv文件
                        count += 1
                        writer.writerow({
                            'Index': count,
                            'Project': project,
                            'Filename': filename,
                            'Path': path,
                            'Author': author_name,
                            'Keyword': keyword
                        })
