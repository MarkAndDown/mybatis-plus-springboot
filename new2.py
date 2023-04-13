import os
import re
import xlwt

# 递归查找指定文件类型的文件
def find_files(root, extensions):
    for subdir, dirs, files in os.walk(root):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if ext in extensions:
                yield os.path.join(subdir, file)

# 在文件中查找指定字符串
def search_file(file_path, search_str):
    with open(file_path, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            if re.search(search_str, line):
                return i+1  # 返回行数
    return -1  # 没有找到

# 获取文件名
def get_file_name(file_path):
    return os.path.basename(file_path)

# 获取文件路径去掉SourceTree之前的内容
def get_file_path(file_path):
    index = file_path.find("SourceTree")
    if index >= 0:
        return file_path[index+len("SourceTree")+1:]
    return file_path

# 生成Excel文件
def generate_excel(results):
    workbook = xlwt.Workbook(encoding="utf-8")
    sheet = workbook.add_sheet("Result")

    # 写入表头
    sheet.write(0, 0, "ID")
    sheet.write(0, 1, "Type")
    sheet.write(0, 2, "File Name")
    sheet.write(0, 3, "File Path")
    sheet.write(0, 4, "Danny")
    sheet.write(0, 5, "Search String")

    # 写入数据
    for i, result in enumerate(results):

        sheet.write(i+1, 1, "CSMS" if result["Type"] in [".jsp", ".java"] else "CIS")
        sheet.write(i+1, 2, result["File Name"])
        sheet.write(i+1, 3, result["File Path"])
        sheet.write(i+1, 4, "Danny")
        sheet.write(i+1, 5, result["Search String"])

    workbook.save("result.xls")

# 搜索指定字符串并输出结果到Excel表格
def search_and_output(paths, extensions, search_strs):
    results = []
    file_names = set()  # 用于去重

    for search_str in search_strs:
        # 按照文件类型排序
        result = {
            "Type": "",
            "File Name": "",
            "File Path": "",
            "Search String": search_str
        }
        results.append(result)
        for path in paths:
            for file_path in find_files(path, extensions):
                file_name = get_file_name(file_path)
                if (search_str,file_name,path) in file_names:  # 如果已经处理过该文件，则跳过
                    continue
                file_names.add(file_name)
                line_num = search_file(file_path, search_str)
                if line_num >= 0:
                    result = {
                        "Type": os.path.splitext(file_path)[-1],
                        "File Name": file_name,
                        "File Path": get_file_path(file_path),
                        "Search String": search_str
                    }
                    results.append(result)


    # 生成Excel文件
    workbook = xlwt.Workbook(encoding="utf-8")
    sheet = workbook.add_sheet("Result")
    # 写入表头
    sheet.write(0, 0, "ID")
    sheet.write(0, 1, "Type")
    sheet.write(0, 2, "File Name")
    sheet.write(0, 3, "File Path")
    sheet.write(0, 4, "Danny")
    sheet.write(0, 5, "Search String")
    # 写入数据
    for i, result1 in enumerate(results):
        if (len(result1["File Name"])==0 and len(result1["File Path"])==0):
            sheet.write_merge(i + 1, i + 1, 0, 5, result["Search String"])
            continue
        sheet.write(i + 1, 0, i + 1)
        sheet.write(i + 1, 1, "CSMS" if result1["Type"] in [".jsp", ".java"] else "CIS")
        sheet.write(i + 1, 2, result1["File Name"])
        sheet.write(i + 1, 3, result1["File Path"])
        sheet.write(i + 1, 4, "Danny")
        sheet.write(i + 1, 5, result1["Search String"])

    workbook.save("result.xls")

# 测试代码


if __name__ == "__main__":
    paths = ["E:/test/SourceTree/cca", "E:/test/SourceTree/fd"]
    extensions = [".java", ".sql", ".jsp", ".PLSQL"]
    # 定义要查找的字符串
    search_strs = ["PRD_18661", "PRD_18568"]

    search_and_output(paths, extensions,search_strs)
