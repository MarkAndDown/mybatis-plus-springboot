import tkinter as tk
import git
import os
import paramiko

def extract_code():
    # 获取输入框中的值
    repo_path = entry_repo_path.get()
    commit_start = entry_commit_start.get()
    commit_end = entry_commit_end.get()
    output_folder = entry_output_folder.get()

    # 切换到仓库目录
    os.chdir(repo_path)

    # 初始化 Git 仓库
    repo = git.Repo(repo_path)

    # 执行 git pull 命令，将代码拉取到最新状态
    repo.remotes.origin.pull()

    # 获取两个 commit 之间的差异
    diff_index = repo.commit(commit_end).diff(commit_start)

    # 提取差异的文件到新文件夹
    os.makedirs(output_folder, exist_ok=True)

    for diff in diff_index.iter_change_type('M'):  # 只提取修改的文件
        file_content = diff.a_blob.data_stream.read()  # 获取文件内容
        file_path = os.path.join(output_folder, diff.a_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(file_content)

    # 提示用户抽取完成
    tk.messagebox.showinfo("Information", "Code extracted successfully!")

def upload_and_execute():
    # 获取输入框中的值
    output_folder = entry_output_folder.get()
    server_ip = entry_server_ip.get()
    username = entry_username.get()
    password = entry_password.get()
    remote_folder = entry_remote_folder.get()
    job_command = entry_job_command.get()

    # 连接到远程服务器
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=server_ip, username=username, password=password)

    # 使用 SFTP 上传文件到远程服务器
    sftp_client = ssh_client.open_sftp()
    local_files = os.listdir(output_folder)
    for local_file in local_files:
        local_file_path = os.path.join(output_folder, local_file)
        remote_file_path = os.path.join(remote_folder, local_file)
        sftp_client.put(local_file_path, remote_file_path)

    # 关闭 SFTP 连接
    sftp_client.close()

    # 关闭 SSH 连接
    ssh_client.close()

    # 提示用户上传完成
    tk.messagebox.showinfo("Information", "Code uploaded successfully!")

    # 连接到远程服务器并切换到指定文件夹
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=server_ip, username=username, password=password)

    # 执行命令，cd 到指定文件夹并执行任务
    command = f"cd {remote_folder}; {job_command}"
    stdin, stdout, stderr = ssh_client.exec_command(command)

    # 获取命令执行结果并显示
    result = stdout.read().decode("utf-8")
    tk.messagebox.showinfo("Job Execution Result", result)

    # 关闭 SSH 连接
    ssh_client.close()

# 创建主窗口
root = tk.Tk()
root.title("Git Files Upload")

# 创建输入框和标签
labels = ["Local Repository Path:", "Commit Start:", "Commit End:", "Output Folder:", "Server IP:", "Username:", "Password:", "Remote Folder:", "Job Command:"]
entries = []
for i, label_text in enumerate(labels):
    label = tk.Label(root, text=label_text)
    label.grid(row=i, column=0, padx=5, pady=5)

    entry = tk.Entry(root)
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries.append(entry)

# 创建抽取代码按钮
extract_button = tk.Button(root, text="Extract Code", command=extract_code)
extract_button.grid(row=len(labels)+1, column=0, padx=5, pady=5)

# 创建上传并执行任务按钮
upload_button = tk.Button(root, text="Upload & Execute Job", command=upload_and_execute)
upload_button.grid(row=len(labels)+1, column=1, padx=5, pady=5)

root.mainloop()
