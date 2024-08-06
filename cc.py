import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import git
import paramiko
import os
from datetime import datetime
import threading

class RemoteServer:
    def __init__(self):
        self.ssh = None
        self.sftp = None

    def connect(self, server_ip, username, password):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(server_ip, username=username, password=password)
            self.sftp = self.ssh.open_sftp()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {e}")
            return False

    def disconnect(self):
        if self.sftp:
            self.sftp.close()
        if self.ssh:
            self.ssh.close()

    def execute_command(self, command, log_text_widget, log_file_path):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            for line in iter(stdout.readline, ""):
                log_text_widget.insert(tk.END, line)
                log_text_widget.see(tk.END)
                with open(log_file_path, 'a') as log_file:
                    log_file.write(line)
            for line in iter(stderr.readline, ""):
                log_text_widget.insert(tk.END, line)
                log_text_widget.see(tk.END)
                with open(log_file_path, 'a') as log_file:
                    log_file.write(line)
        except Exception as e:
            messagebox.showerror("Error", f"Command execution failed: {e}")

# 功能1：从Git仓库中提取两个commit之间的代码
def extract_commits():
    repo_path = entry_repo_path.get()
    commit1 = entry_commit1.get()
    commit2 = entry_commit2.get()
    output_dir = entry_output_dir.get()

    if not repo_path or not commit1 or not commit2 or not output_dir:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    try:
        repo = git.Repo(repo_path)
        diffs = repo.git.diff(commit1, commit2, '--name-only')
        file_list = diffs.split('\n')
        
        # 生成日期和commit前6位的文件夹名称
        today = datetime.today().strftime('%Y%m%d')
        folder_name = f"{today}_{commit1[:6]}_{commit2[:6]}"
        output_path = os.path.join(output_dir, folder_name)
        os.makedirs(output_path, exist_ok=True)

        for file in file_list:
            if file:
                src_path = os.path.join(repo_path, file)
                dest_path = os.path.join(output_path, file)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with open(src_path, 'rb') as src_file, open(dest_path, 'wb') as dest_file:
                    dest_file.write(src_file.read())
        
        messagebox.showinfo("Completed", f"Code extraction completed. Files saved to {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Extraction failed: {e}")

# 功能2：将提取的代码以二进制方式上传到服务器的固定文件夹
def upload_to_server():
    local_path = entry_local_path.get()
    server_ip = entry_server_ip.get()
    server_username = entry_server_username.get()
    server_password = entry_server_password.get()
    remote_path = entry_remote_path.get()

    if not local_path or not server_ip or not server_username or not server_password or not remote_path:
        messagebox.showerror("Error", "Please fill in all fields")
        return

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
                with open(local_file, 'rb') as f:
                    sftp.putfo(f, remote_file)
        
        sftp.close()
        ssh.close()
        
        messagebox.showinfo("Completed", "File upload completed")
    except Exception as e:
        messagebox.showerror("Error", f"Upload failed: {e}")

# 功能3：连接远程服务器并提交作业
def login_server():
    server_ip = entry_job_server_ip.get()
    server_username = entry_job_server_username.get()
    server_password = entry_job_server_password.get()

    if not server_ip or not server_username or not server_password:
        messagebox.showerror("Error", "Please fill in all fields")
        return
    
    if remote_server.connect(server_ip, server_username, server_password):
        log_text.insert(tk.END, "Login successful\n")

def execute_command():
    job_command = entry_job_command.get()
    if not job_command:
        messagebox.showerror("Error", "Please enter a command")
        return
    
    log_file_path = "server_log.txt"  # 保存日志的文件
    threading.Thread(target=remote_server.execute_command, args=(job_command, log_text, log_file_path)).start()

# 创建主窗口
root = tk.Tk()
root.title("Git Operations and Remote Server Management")

# 创建Notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# 第一个标签：提取Git代码
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text="Extract Git Code")

label_repo_path = tk.Label(frame1, text="Git Repository Path:")
label_repo_path.pack()
entry_repo_path = tk.Entry(frame1, width=40)
entry_repo_path.pack(pady=5)

label_commit1 = tk.Label(frame1, text="First Commit:")
label_commit1.pack()
entry_commit1 = tk.Entry(frame1, width=40)
entry_commit1.pack(pady=5)

label_commit2 = tk.Label(frame1, text="Second Commit:")
label_commit2.pack()
entry_commit2 = tk.Entry(frame1, width=40)
entry_commit2.pack(pady=5)

label_output_dir = tk.Label(frame1, text="Output Directory:")
label_output_dir.pack()
entry_output_dir = tk.Entry(frame1, width=40)
entry_output_dir.pack(pady=5)

button_extract = tk.Button(frame1, text="Extract Code", command=extract_commits)
button_extract.pack(pady=5)

# 第二个标签：上传代码到服务器
frame2 = ttk.Frame(notebook)
notebook.add(frame2, text="Upload Code to Server")

label_local_path = tk.Label(frame2, text="Local Path:")
label_local_path.pack()
entry_local_path = tk.Entry(frame2, width=40)
entry_local_path.pack(pady=5)

label_server_ip = tk.Label(frame2, text="Server IP:")
label_server_ip.pack()
entry_server_ip = tk.Entry(frame2, width=40)
entry_server_ip.pack(pady=5)

label_server_username = tk.Label(frame2, text="Username:")
label_server_username.pack()
entry_server_username = tk.Entry(frame2, width=40)
entry_server_username.pack(pady=5)

label_server_password = tk.Label(frame2, text="Password:")
label_server_password.pack()
entry_server_password = tk.Entry(frame2, width=40, show='*')
entry_server_password.pack(pady=5)

label_remote_path = tk.Label(frame2, text="Remote Path:")
label_remote_path.pack()
entry_remote_path = tk.Entry(frame2, width=40)
entry_remote_path.pack(pady=5)

button_upload = tk.Button(frame2, text="Upload Code", command=upload_to_server)
button_upload.pack(pady=5)

# 第三个标签：提交作业
frame3 = ttk.Frame(notebook)
notebook.add(frame3, text="Submit Job")

label_job_server_ip = tk.Label(frame3, text="Job Server IP:")
label_job_server_ip.pack()
entry_job_server_ip = tk.Entry(frame3, width=40)
entry_job_server_ip.pack(pady=5)

label_job_server_username = tk.Label(frame3, text="Username:")
label_job_server_username.pack()
entry_job_server_username = tk.Entry(frame3, width=40)
entry_job_server_username.pack(pady=5)

label_job_server_password = tk.Label(frame3, text="Password:")
label_job_server_password.pack()
entry_job_server_password = tk.Entry(frame3, width=40, show='*')
entry_job_server_password.pack(pady=5)

button_login = tk.Button(frame3, text="Login", command=login_server)
button_login.pack(pady=5)

label_job_command = tk.Label(frame3, text="Job Command:")
label_job_command.pack()
entry_job_command = tk.Entry(frame3, width=40)
entry_job_command.pack(pady=5)

button_submit = tk.Button(frame3, text="Submit Job", command=execute_command)
button_submit.pack(pady=5)

log_text = scrolledtext.ScrolledText(frame3, width=60, height=20)
log_text.pack(pady=5)

# 创建远程服务器对象
remote_server = RemoteServer()

# 运行主窗口
root.mainloop()
