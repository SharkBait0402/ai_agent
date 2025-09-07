import os

def get_file_content(working_directory, file_path):
    abs_path = os.path.join(working_directory, file_path)
    dir_path = os.path.abspath(abs_path)
    work_path = os.path.abspath(working_directory)
    if not dir_path.startswith(work_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(abs_path):
        return f"Error: File not found or is not a regular file"
        
    max_chars = 10000

    with open(abs_path, "r") as f:
        file_content_string = f.read(max_chars)

    return file_content_string

print(get_file_content("calculator", "pkg/calculator.py"))
