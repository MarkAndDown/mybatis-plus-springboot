import git
import os
import shutil

# 本地 Git 仓库路径
repo_path = '/path/to/your/repository'

# 切换到仓库目录
os.chdir(repo_path)

# 初始化 Git 仓库
repo = git.Repo(repo_path)

# 执行 git pull 命令，将代码拉取到最新状态
repo.remotes.origin.pull()

# 两个 commit 的 SHA 标识
commit_start = 'commit_start_hash'
commit_end = 'commit_end_hash'

# 获取两个 commit 之间的差异
diff_index = repo.commit(commit_end).diff(commit_start)

# 提取差异的文件到新文件夹
output_folder = '/path/to/new_folder'
os.makedirs(output_folder, exist_ok=True)

for diff in diff_index.iter_change_type('M'):  # 只提取修改的文件
    file_content = diff.a_blob.data_stream.read()  # 获取文件内容
    file_path = os.path.join(output_folder, diff.a_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(file_content)
