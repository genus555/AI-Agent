import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def VerbosePrint(response, user_prompt):
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def main():

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

    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages,)

    if verbose_mode:
        VerbosePrint(response, user_prompt)
    print(response.text)

if __name__ == "__main__":
    main()
