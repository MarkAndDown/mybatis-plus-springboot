import os
import pandas as pd

# 定义需要递归查找的路径列表
paths = ["C:/CSMS/back/fd/dss/f", "D:/", "E:/"]

# 定义需要查找的文件类型
file_types = (".java", ".sql", ".jsp", ".PLSQL")

# 定义需要查找的字符串列表
search_strings = ["PRD_18661", "PRD_18568"]

# 定义输出文件名
output_file = "output.xlsx"

# 定义列名列表
columns = ["包含的字符", "类型", "文件名", "路径", "Danny", "IFP_23_RL02_PRD_18861"]

# 定义结果列表
result = []

# 递归查找文件并处理
def search_files(path, search_strings, file_types):
    for root, dirs, files in os.walk(path):
        for file in files:
            # 判断文件类型
            if file.endswith(file_types):
                # 判断文件内容是否包含搜索字符串
                with open(os.path.join(root, file), "rb") as f:
                    content = f.read().decode(errors="ignore")  # 忽略无法解码的字符
                    if any(search_string in content for search_string in search_strings):
                        # 获取文件名和文件路径
                        file_name = os.path.basename(file)
                        file_path = os.path.join(root, file)[len("SourceTree"):]

                        # 判断文件类型并设置第二列的值
                        if file.endswith((".jsp", ".java")):
                            col2 = "CSMS"
                        else:
                            col2 = "CIS"

                        # 添加到结果列表中
                        result.append([search_strings[0] + "或" + search_strings[1], col2, file_name, file_path, "Danny", "IFP_23_RL02_PRD_18861"])

# 查找文件并处理
for path in paths:
    search_files(path, search_strings, file_types)

# 将结果去重并按照文件类型排序
df = pd.DataFrame(result, columns=columns)
df.drop_duplicates(subset=["文件名", "路径"], keep="first", inplace=True)
df.sort_values(by=["类型", "文件名"], ascending=True, inplace=True)

# 将结果写入Excel表格
df.to_excel(output_file, index_label="序号", startrow=1)
# 写入包含的字符到第一行
with pd.ExcelWriter(output_file, mode='a') as writer:
    df_char = pd.DataFrame({"包含的字符": [search_strings[0] + "或" + search_strings[1]]})
    df_char.to_excel(writer, index_label="序号")
