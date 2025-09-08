import os
from google.genai import types 


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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of a given file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read the content of",
            ),
        },
    ),
)

