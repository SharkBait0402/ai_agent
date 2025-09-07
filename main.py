import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types 
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


if len(sys.argv) < 2:
    print("Error: Prompt not provided")
    sys.exit(1)


prompt = sys.argv[1]

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

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

messeges = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

def main():

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messeges,
       config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
        )
    )

    if response.function_calls:
        for fc in response.function_calls:
            print(f"Calling function: {fc.name}({fc.args})")
            if fc.name == "schema_get_files_info":
                result = get_files_info(**fc.args)
                print(result)
            elif fc.name == "schema_get_file_content":
                result = get_file_content(**fc.args)
                print(result)  # ensure get_files_info returns a value
            elif fc.name == "schema_write_file":
                result = write_file(**fc.args)
                print(result)  # ensure get_files_info returns a value
            elif fc.name == "schema_run_python_file":
                result = run_python_file(**fc.args)
                print(result)  # ensure get_files_info returns a value


    else:
        print(response.text)


    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        print(f"User prompt: {prompt}")

        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")

        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()
