import git
import re
from datetime import datetime, timedelta

# 设置Git仓库路径
repo_path = '/path/to/your/git/repo'

# 创建Git仓库对象
repo = git.Repo(repo_path)

# 定义时间范围，例如，两个月之前到现在的时间段
end_date = datetime.now()
start_date = end_date - timedelta(days=60)

# 用于存储符合条件的文件
matching_files = set()

# 遍历提交记录
for commit in repo.iter_commits(since=start_date, until=end_date):
    for diff in commit.diff():
        # 获取文件的路径
        file_path = diff.a_path or diff.b_path

        # 检查文件是否包含 "PPP-111"，并且是否包含 "ddd_222"
        if re.search(r'PPP-111', diff.diff.decode('utf-8'), re.IGNORECASE) and re.search(r'ddd_222', diff.diff.decode('utf-8'), re.IGNORECASE):
            matching_files.add(file_path)

# 打印符合条件的文件列表
for file in matching_files:
    print(file)
