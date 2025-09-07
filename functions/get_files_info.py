import os
from google.genai import types 

def get_files_info(working_directory, directory="."):
    file_path = os.path.join(working_directory, directory)
    dir_path = os.path.abspath(file_path)
    work_path = os.path.abspath(working_directory)
    if not dir_path.startswith(work_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    all_files = os.listdir(file_path)
    files = []
    for file in all_files:
        if not file.startswith("."):
            files.append(file)

    tmp_list = []
    for file in files:
        active_file = f"{file_path}/{file}"
        temp = f"- {file}: file_size={os.path.getsize(active_file)}, is_dir={os.path.isdir(active_file)}"
        tmp_list.append(temp)

    file_str = "\n".join(tmp_list)

    return file_str


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
