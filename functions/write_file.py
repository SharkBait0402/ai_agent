import os

def write_file(working_directory, file_path, content):
    abs_path = os.path.join(working_directory, file_path)
    dir_path = os.path.abspath(abs_path)
    work_path = os.path.abspath(working_directory)

    if not dir_path.startswith(work_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(file_path):
        os.mknod(file_path)

    with open(file_path, "w") as f:
        f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'



