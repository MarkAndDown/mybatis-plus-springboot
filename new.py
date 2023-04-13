import os
import csv

# Define the file extensions to search for
extensions = ('.java', '.sql', '.jsp', '.PLSQL')

# Define the search string
search_string = 'PRD_18661'

# Define the output file name
output_file = 'output.csv'

# Define the header for the output file
header = ['No.', 'System', 'File Name', 'File Path', 'Created By', 'Title']

# Define the systems for display based on file extension
system_dict = {'.java': 'CSMS', '.sql': 'CIS', '.jsp': 'CIS', '.PLSQL': 'CIS'}

# Initialize the list to store the file paths and names
file_list = []

# Define the recursive function to search for files with specified extensions and containing the search string
def search_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extensions) and search_string in open(os.path.join(root, file)).read():
                # Remove the characters before the 5th backslash in the file path
                file_path = os.path.join(root, file)
                file_path_parts = file_path.split('\\')
                file_path = '\\'.join(file_path_parts[5:])
                
                # Get the system name based on the file extension
                system = system_dict.get(os.path.splitext(file)[1], '')
                
                # Append the file path and name to the list
                file_list.append((file, file_path, system))

# Search the specified paths for files with the specified extensions and containing the search string
for path in ['C:/CSMS/back/fd/dss/f', 'D://', 'E://']:
    search_files(path)

# Remove duplicates from the list of file paths and names
file_list = list(set(file_list))

# Sort the list of file paths and names by file extension
file_list = sorted(file_list, key=lambda x: os.path.splitext(x[0])[1])

# Write the output to a CSV file
with open(output_file, mode='w', newline='') as output:
    writer = csv.writer(output)
    writer.writerow(header)
    for i, file in enumerate(file_list, start=1):
        row = [i]
        if file[2] != '':
            row.append(file[2])
        else:
            row.append('')
        row.append(file[0])
        row.append(file[1])
        row.append('Danny')
        row.append('IFP_23_RL02_PRD_18861')
        writer.writerow(row)
