import os
from google.genai import types 
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

functions = {
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
    "get_file_content": get_file_content,
}

def call_function(function_call_part, verbose=False):
    if verbose==True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    func = functions.get(function_name)
    if func == None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )

    kwargs = dict(function_call_part.args or {})
    kwargs["working_directory"] = "./calculator"
    function_result = func(**kwargs)
        
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
                )
            ],
        )

