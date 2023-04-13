import os
import csv

# 定义要查找的路径
search_paths = ["C:/CSMS/back/fd", "D:/", "E:/"]
# 定义要查找的文件类型后缀
extensions = [".java", ".sql", ".jsp", ".PLSQL"]
# 定义要查找的字符串
target_string = "PRD_18661"

# 定义输出的csv文件名和列名
output_file = "search_result.csv"
field_names = ["序号", "系统", "文件名", "文件路径"]

# 定义系统名映射
system_map = {
    ".jsp.java": "CSMS",
}

# 初始化行号
row_number = 1

# 定义输出结果的列表
result_list = []

# 遍历所有路径和文件
for search_path in search_paths:
    for dirpath, dirnames, filenames in os.walk(search_path):
        for filename in filenames:
            # 判断文件后缀是否符合要求
            if any(filename.endswith(ext) for ext in extensions):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if target_string in content:
                            system_name = "CIS"
                            for ext in system_map:
                                if filename.endswith(ext):
                                    system_name = system_map[ext]
                                    break
                            result_list.append([row_number, system_name, filename, file_path])
                            row_number += 1
                except:
                    pass

# 对结果按照文件类型排序
result_list.sort(key=lambda x: extensions.index(os.path.splitext(x[2])[1]))

# 输出结果到csv文件
with open(output_file, "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(field_names)
    writer.writerows(result_list)
