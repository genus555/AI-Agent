import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
import argparse
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def VerbosePrint(response, user_prompt):
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def main():

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
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

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    content = sys.argv

    #adding optional --argparse command line argument
    parser = argparse.ArgumentParser()

    if len(content) > 1:
        parser.add_argument("prompt", help=content)
    else:
        print("ERROR")
        sys.exit(1)

    parser.add_argument("--verbose", action="store_true",)
    args = parser.parse_args()
    user_prompt = args.prompt
    verbose_mode = args.verbose
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),)

    if response.function_calls == []:

        if verbose_mode:
            VerbosePrint(response, user_prompt)
        print(response.text)
    
    else:
        for function_call in response.function_calls:
            try:
                
                function_call_results = call_function(function_call)
                
                if verbose_mode:
                    print(f"-> {function_call_results.parts[0].function_response.response}")
                
                else:
                    print(function_call_results.parts[0].function_response.response['result'])

            except Exception as e:
                print(f"Something went wrong: {e}")

if __name__ == "__main__":
    main()
