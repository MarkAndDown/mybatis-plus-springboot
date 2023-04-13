import os
import csv

# Define the paths to search
paths_to_search = ["C:/CSMS/back/fd/dss/f", "D:/", "E:/"]

# Define the file extensions to look for
file_extensions = [".java", ".sql", ".jsp", ".PLSQL"]

# Define the string to search for in the files
search_string = "PRD_18661"

# Define the CSV file name and headers
csv_file_name = "file_data.csv"
csv_headers = ["No.", "Type", "Name", "Path", "Author", "Title"]

# Initialize a list to store the file data
file_data = []

# Define a function to process each file found
def process_file(file_path):
    # Check if file has the desired extension
    if os.path.splitext(file_path)[1] in file_extensions:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            # Check if file contains the desired string
            if search_string in f.read():
                # Extract the desired data from the file path
                path_parts = file_path.split("/")
                file_name = path_parts[-1]
                file_path = "/".join(path_parts[4:])
                file_type = os.path.splitext(file_name)[1]
                if file_type == ".jsp" or file_type == ".java":
                    file_type_display = "CSMS"
                else:
                    file_type_display = "CIS"
                author = "Danny"
                title = "IFP_23_RL02_PRD_18861"
                # Add the file data to the list
                file_data.append([len(file_data)+1, file_type_display, file_name, file_path, author, title])

# Recursively search for files in the specified paths
for path in paths_to_search:
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            process_file(os.path.join(dirpath, filename))

# Remove duplicates from file data
file_data = list(set(map(tuple, file_data)))

# Sort the file data by file type
file_data.sort(key=lambda x: x[1])

# Write the file data to a CSV file
with open(csv_file_name, "w", newline="", encoding="utf-8") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(csv_headers)
    csv_writer.writerows(file_data)
