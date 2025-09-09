import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types 
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


if len(sys.argv) < 2:
    print("Error: Prompt not provided")
    sys.exit(1)


prompt = sys.argv[1]
verbose = False

if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
    verbose = True


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schema_get_file_content,
        schema_write_file,
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory which is calculator. However, you do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

messeges = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

def main():

    for i in range(0,20):

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=messeges,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
                )
            )
        except Exception as e:
            print(f"Error: {e}")

        try:
            for candidate in response.candidates:
                messeges.append(candidate.content)

            if response.function_calls:
                for fc in response.function_calls:
                    try:
                        function_call_result = call_function(fc, verbose=verbose)
                        function_response = function_call_result.parts[0].function_response.response["result"]
                        var = types.Content(
                            role="user",
                            parts=[types.Part(text=function_response)]
                            )
                        messeges.append(var)

                    except Exception as e:
                        var = types.Content(
                            role="user",
                            parts=[types.Part(text=str(e))]
                            )
                        messeges.append(var)
                continue
        except Exception as e :
            print("an error has occured")

        if response.text != "":
            print(response.text)
            break



            # print(f"-> {function_call_result.parts[0].function_response.response["result"]}")


    else:
        print(response.text)


    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        print(f"User prompt: {prompt}")

        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")

        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()
