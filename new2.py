import os
import openpyxl

# 要递归查找的文件夹路径列表
path_list = ["C:/CSMS/back/fd/dss/f", "D:/", "E:/"]

# 需要查找的文件类型列表
extension_list = [".java", ".sql", ".jsp", ".PLSQL"]

# 包含的字符列表
include_list = ["PRD_18661", "PRD_18568"]

# 初始化结果列表
result_list = []

# 定义函数，递归查找符合条件的文件并添加到结果列表
def search_files(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(tuple(extension_list)):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if any(x in content for x in include_list):
                        # 获取文件名和文件路径，去掉SourceTree之前的内容
                        filename_only = os.path.basename(filepath)
                        filepath_only = filepath.split("SourceTree")[1]
                        # 添加到结果列表
                        result_list.append([filename_only, filepath_only])

# 遍历文件夹列表，调用函数递归查找符合条件的文件
for path in path_list:
    search_files(path)

# 去重，按照文件类型排序
result_list = sorted(list(set(tuple(x) for x in result_list)), key=lambda x: (x[1].split(".")[-1], x[1]))

# 创建Excel表格并写入结果
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Search Results"

# 写入表头
header = ["No.", "Type", "File Name", "File Path", "Danny", "IFP_23_RL02_PRD_18861"]
ws.append(header)

# 写入数据
for i, row in enumerate(result_list):
    # 第一列序号从1开始
    row.insert(0, i+1)
    # 如果是.jsp或者.java，则展示CSMS，其他展示CIS
    row[1] = "CSMS" if row[1].endswith((".jsp", ".java")) else "CIS"
    # 添加Danny和IFP_23_RL02_PRD_18861
    row.append("Danny")
    row.append("IFP_23_RL02_PRD_18861")
    ws.append(row)

# 保存Excel表格
wb.save("search_results.xlsx")
