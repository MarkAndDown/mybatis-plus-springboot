import os
import csv

# 要搜索的文件类型
file_types = ['.java', '.sql', '.jsp', '.PLSQL']

# 要搜索的路径
search_paths = ['C:/CSMS/back/fd/dss/f', 'D:/', 'E:/']

# 要搜索的字符串
search_str = 'PRD_18661'

# 保存结果的文件名
output_filename = 'result.csv'

# 递归搜索路径下所有符合要求的文件
def search_files(path):
    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(tuple(file_types)):
                files.append(os.path.join(root, filename))
    return files

# 判断文件中是否包含搜索字符串
def is_file_contain_str(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        contents = f.read()
        return search_str in contents

# 获取文件类型
def get_file_type(file_path):
    ext = os.path.splitext(file_path)[1]
    return ext.lower()

# 判断文件类型是否在要搜索的类型列表中
def is_file_type_in_types(file_type):
    return file_type in file_types

# 主函数
def main():
    result = []
    index = 1
    for path in search_paths:
        files = search_files(path)
        for file_path in files:
            file_type = get_file_type(file_path)
            if is_file_type_in_types(file_type) and is_file_contain_str(file_path):
                row = [index, 'CSMS' if file_type == '.jsp.java' else 'CIS', os.path.basename(file_path), os.path.dirname(file_path)]
                result.append(row)
                index += 1
    result = sorted(result, key=lambda x: file_types.index(get_file_type(x[2])))
    # 写入csv文件
    with open(output_filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['序号', '系统名称', '文件名', '文件路径'])
        for row in result:
            writer.writerow(row)

if __name__ == '__main__':
    main()
