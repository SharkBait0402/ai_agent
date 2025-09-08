import os
from google.genai import types 

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

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrite the contents of a file with a new contents or create a new file if one is not already there",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File to overwrite the contents of, if not file is there, create a new one",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="contents to overwrite to new file",
            ),
        },
    ),
)
