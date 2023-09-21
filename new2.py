import git
import re
from datetime import datetime, timedelta

# 设置Git仓库路径
repo_path = '/path/to/your/git/repo'

# 创建Git仓库对象
repo = git.Repo(repo_path)

# 计算一个月前的日期
one_month_ago = datetime.now() - timedelta(days=30)

# 用于存储匹配的文件的集合
matching_files_set = set()

# 遍历最近一个月的提交记录
for commit in repo.iter_commits(since=one_month_ago):
    commit_message = commit.message.lower()  # 将提交备注转为小写，以便进行匹配

    # 检查提交备注是否包含 "PPP-111"
    if "ppp-111" in commit_message:
        # 遍历提交的文件差异
        for diff in commit.diff():
            # 获取文件的路径
            file_path = diff.a_path or diff.b_path

            try:
                # 打开文件并逐行检查是否包含 "DDD_222"
                with open(file_path, 'r', encoding='utf-8') as file_content:
                    lines = file_content.readlines()
                    for line in lines:
                        if re.search(r'ddd_222', line, re.IGNORECASE):
                            matching_files_set.add(file_path)
                            break  # 如果文件中包含一行即可满足条件，可以提前结束对该文件的检查
            except FileNotFoundError:
                # 如果无法打开文件，跳过该文件的处理
                pass

# 定义不同类别的文件字典
file_categories = {
    "rule": [],
    "constant": [],
    "util": [],
    "mapper": [],
    "domain": [],
    "vo": [],
    "dml": [],
    "test": []
}

# 遍历匹配的文件列表，并根据文件路径中的字符分类
for file_path in matching_files_set:
    if "rule" in file_path.lower():
        file_categories["rule"].append(file_path)
    elif "constant" in file_path.lower():
        file_categories["constant"].append(file_path)
    elif "util" in file_path.lower():
        file_categories["util"].append(file_path)
    elif "mapper" in file_path.lower():
        file_categories["mapper"].append(file_path)
    elif "domain" in file_path.lower():
        file_categories["domain"].append(file_path)
    elif "vo" in file_path.lower():
        file_categories["vo"].append(file_path)
    elif "dml" in file_path.lower():
        file_categories["dml"].append(file_path)
    elif "test" in file_path.lower():
        file_categories["test"].append(file_path)

# 打印分类后的文件列表
for category, files in file_categories.items():
    print(f"{category.capitalize()} Files:")
    for file in files:
        print(f"  - {file}")
