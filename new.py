from git import Repo
from datetime import datetime

# 指定本地Git仓库的路径
repo_path = 'path/to/your/repository'

# 打开Git仓库
repo = Repo(repo_path)

# 指定作者的名称
author_name = 'Author Name'

# 指定起始日期和结束日期
start_date = datetime(2023, 1, 1)  # 指定起始日期
end_date = datetime(2023, 12, 31)  # 指定结束日期

# 创建集合来跟踪已打印的文件路径
printed_files = set()

# 获取Git日志
log = repo.git.log('--author=' + author_name, '--name-status', '--since=' + start_date.strftime('%Y-%m-%d'), '--until=' + end_date.strftime('%Y-%m-%d'))

# 遍历日志条目
for entry in log.split('\n\n'):
    commit_info, file_changes = entry.split('\n', 1)
    commit_hash, commit_message = commit_info.split('\n', 1)
    file_changes = file_changes.strip().split('\n')
    
    # 检查是否有文件改动，如果没有则忽略本次commit
    if len(file_changes) == 0:
        continue
    
    print(f"提交ID: {commit_hash}")
    print(f"提交消息: {commit_message}")
    print("改动文件:")
    for change in file_changes:
        change_type, file_path = change.split('\t', 1)
        if file_path not in printed_files:
            print(f"  类型: {change_type}\t路径: {file_path}")
            printed_files.add(file_path)
            
            # 读取文件内容
            with open(file_path, 'r') as file:
                content = file.read()
                
                # 提取注释含有"add"的行
                print("注释含有'add'的行:")
                for line in content.split('\n'):
                    if line.strip().startswith('#') and 'add' in line:
                        print(line)
                        
                # 提取注释含有"start"和"end"之间的代码块
                print("注释含有'start'和'end'之间的代码块:")
                start_found = False
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith('# start'):
                        start_found = True
                        print(line)
                    elif line.startswith('# end'):
                        start_found = False
                        print(line)
                    elif start_found:
                        print(line)
                
    print('---')
