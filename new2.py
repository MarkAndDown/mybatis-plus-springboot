import git
import re
from datetime import datetime, timedelta

# 设置Git仓库路径
repo_path = '/path/to/your/git/repo'

# 创建Git仓库对象
repo = git.Repo(repo_path)

# 计算一个月前的日期
one_month_ago = datetime.now() - timedelta(days=30)

# 用于存储匹配的提交记录和文件
matching_commits = []

# 遍历最近一个月的提交记录
for commit in repo.iter_commits(since=one_month_ago):
    commit_message = commit.message.lower()  # 将提交备注转为小写，以便进行匹配

    # 检查提交备注是否包含 "PPP-111"
    if "ppp-111" in commit_message:
        matching_files = set()

        # 遍历提交的文件差异
        for diff in commit.diff():
            # 获取文件的路径
            file_path = diff.a_path or diff.b_path

            # 打开文件并逐行检查是否包含 "DDD_222"
            with open(file_path, 'r', encoding='utf-8') as file_content:
                lines = file_content.readlines()
                for line in lines:
                    if re.search(r'ddd_222', line, re.IGNORECASE):
                        matching_files.add(file_path)
                        break  # 如果文件中包含一行即可满足条件，可以提前结束对该文件的检查

        # 如果匹配的文件不为空，则将提交记录添加到匹配的提交记录列表中
        if matching_files:
            matching_commits.append({
                "commit": commit,
                "matching_files": matching_files
            })

# 打印匹配的提交记录和对应的文件
for match in matching_commits:
    print(f"Commit SHA: {match['commit'].hexsha}")
    print(f"Commit Message: {match['commit'].message}")
    print("Matching Files:")
    
    # 遍历匹配的文件
    for file in match['matching_files']:
        print(f"  - {file}")

    print()
