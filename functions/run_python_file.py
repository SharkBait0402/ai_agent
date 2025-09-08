import os
import subprocess
import sys
from google.genai import types 

def run_python_file(working_directory, file_path, args=[]):
    abs_path = os.path.join(working_directory, file_path)
    dir_path = os.path.abspath(abs_path)
    work_path = os.path.abspath(working_directory)
    if not dir_path.startswith(work_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'    
    elif not os.path.isfile(abs_path):
        return f"Error: File \"{file_path}\" not found"
    elif not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    new_args = [sys.executable, abs_path, *args]
    for arg in args:
        new_args.append(arg)
    
    obj = subprocess.run(new_args, timeout=30, capture_output=True )

    stdout = (obj.stdout or b"").decode()
    stderr = (obj.stderr or b"").decode()
    
    if obj.returncode != 0:
        return f"Process exited with code {obj.returncode}"
 
    if stdout.strip() == "" and stderr.strip() != "":
        # some runners print to stderr
        return f"STDERR: {stderr}"
    
    if stdout.strip() == "":
        return "no output produced"

    return f"STDOUT: {obj.stdout}\n\n STDERR: {obj.stderr}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a given python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File to run in python",
            ),
        },
    ),
)
