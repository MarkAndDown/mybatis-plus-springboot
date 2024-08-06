import tkinter as tk
from tkinter import filedialog, messagebox
import git
import paramiko
import os


# 功能1：从Git仓库中提取两个commit之间的代码
def extract_commits():
    repo_path = filedialog.askdirectory(title="选择Git仓库目录")
    if not repo_path:
        return
    commit1 = entry_commit1.get()
    commit2 = entry_commit2.get()
    repo = git.Repo(repo_path)
    diffs = repo.git.diff(commit1, commit2, '--name-only')
    file_list = diffs.split('\n')

    output_dir = filedialog.askdirectory(title="选择输出目录")
    if not output_dir:
        return

    for file in file_list:
        if file:
            src_path = os.path.join(repo_path, file)
            dest_path = os.path.join(output_dir, file)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(src_path, 'rb') as src_file, open(dest_path, 'wb') as dest_file:
                dest_file.write(src_file.read())

    messagebox.showinfo("完成", "代码提取完成")


# 功能2：将提取的代码上传到服务器的固定文件夹
def upload_to_server():
    local_path = filedialog.askdirectory(title="选择要上传的目录")
    if not local_path:
        return
    server_ip = entry_server_ip.get()
    server_username = entry_server_username.get()
    server_password = entry_server_password.get()
    remote_path = entry_remote_path.get()

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_ip, username=server_username, password=server_password)
        sftp = ssh.open_sftp()

        for root, dirs, files in os.walk(local_path):
            for file in files:
                local_file = os.path.join(root, file)
                remote_file = os.path.join(remote_path, os.path.relpath(local_file, local_path))
                remote_dir = os.path.dirname(remote_file)
                try:
                    sftp.stat(remote_dir)
                except FileNotFoundError:
                    sftp.mkdir(remote_dir)
                sftp.put(local_file, remote_file)

        sftp.close()
        ssh.close()

        messagebox.showinfo("完成", "文件上传完成")
    except Exception as e:
        messagebox.showerror("错误", f"上传失败：{e}")


# 功能3：连接远程服务器并提交作业
def submit_job():
    server_ip = entry_job_server_ip.get()
    server_username = entry_job_server_username.get()
    server_password = entry_job_server_password.get()
    job_command = entry_job_command.get()

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_ip, username=server_username, password=server_password)
        stdin, stdout, stderr = ssh.exec_command(job_command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        ssh.close()

        if error:
            messagebox.showerror("错误", f"作业提交失败：{error}")
        else:
            messagebox.showinfo("完成", f"作业提交成功：{output}")
    except Exception as e:
        messagebox.showerror("错误", f"作业提交失败：{e}")


# 创建主窗口
root = tk.Tk()
root.title("Git操作与远程服务器管理")

# 第一个标签：提取Git代码
frame1 = tk.Frame(root)
frame1.pack(pady=10)

label1 = tk.Label(frame1, text="提取Git代码")
label1.pack()

entry_commit1 = tk.Entry(frame1, width=40)
entry_commit1.pack(pady=5)
entry_commit1.insert(0, "输入第一个commit")

entry_commit2 = tk.Entry(frame1, width=40)
entry_commit2.pack(pady=5)
entry_commit2.insert(0, "输入第二个commit")

button_extract = tk.Button(frame1, text="提取代码", command=extract_commits)
button_extract.pack(pady=5)

# 第二个标签：上传代码到服务器
frame2 = tk.Frame(root)
frame2.pack(pady=10)

label2 = tk.Label(frame2, text="上传代码到服务器")
label2.pack()

entry_server_ip = tk.Entry(frame2, width=40)
entry_server_ip.pack(pady=5)
entry_server_ip.insert(0, "输入服务器IP")

entry_server_username = tk.Entry(frame2, width=40)
entry_server_username.pack(pady=5)
entry_server_username.insert(0, "输入用户名")

entry_server_password = tk.Entry(frame2, width=40, show='*')
entry_server_password.pack(pady=5)
entry_server_password.insert(0, "输入密码")

entry_remote_path = tk.Entry(frame2, width=40)
entry_remote_path.pack(pady=5)
entry_remote_path.insert(0, "输入远程路径")

button_upload = tk.Button(frame2, text="上传代码", command=upload_to_server)
button_upload.pack(pady=5)

# 第三个标签：提交作业
frame3 = tk.Frame(root)
frame3.pack(pady=10)

label3 = tk.Label(frame3, text="提交作业")
label3.pack()

entry_job_server_ip = tk.Entry(frame3, width=40)
entry_job_server_ip.pack(pady=5)
entry_job_server_ip.insert(0, "输入作业服务器IP")

entry_job_server_username = tk.Entry(frame3, width=40)
entry_job_server_username.pack(pady=5)
entry_job_server_username.insert(0, "输入用户名")

entry_job_server_password = tk.Entry(frame3, width=40, show='*')
entry_job_server_password.pack(pady=5)
entry_job_server_password.insert(0, "输入密码")

entry_job_command = tk.Entry(frame3, width=40)
entry_job_command.pack(pady=5)
entry_job_command.insert(0, "输入作业命令")

button_submit = tk.Button(frame3, text="提交作业", command=submit_job)
button_submit.pack(pady=5)

# 运行主窗口
root.mainloop()
