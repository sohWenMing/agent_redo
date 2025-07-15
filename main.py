#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pprint import pprint
from argument_parsing import parse_flags, get_arg_from_sys_argv, check_verbose_flag
from loading import load_binary
from functions import available_functions, call_function

def main():

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    gemini_api_key = get_api_key()
    # print("gemini_api_key: ", gemini_api_key)
    client = genai.Client(api_key=gemini_api_key)
    
    is_verbose = check_verbose_flag()
    # prompt = types.Part.from_text(text=get_arg_from_user())
    user_prompt = get_arg_from_sys_argv()
    text_part = types.Part.from_text(text=user_prompt)

    # image = load_binary("./test_dog.jpg")
    content  = types.Content(role="user", parts=[text_part])
    contents = [content]

    model = "gemini-2.0-flash-001"
    is_functions_finished = False

    try:
        while is_functions_finished == False: 
            response = gen_content(system_prompt, client, contents, model)
            """
            The sequence of events would be:
                1. we take in the very first prompt, and then we call the generate content action once
                2. If it just comes back with no function calls, we can exit
                3. If not, first we append all the candidates, to the contents
                4. for every function call, we append the return of the function to the contents, before calling the next function
                5. after the last function, we append the last return value of the function, and then we call generate content one more time
            """

            function_calls = response.function_calls

            if function_calls != None:
                candidates = response.candidates
                for candidate in candidates:
                    contents.append(candidate.content)

                for function_call in function_calls:
                    result = call_function(function_call, is_verbose)
                    contents.append(result)
                    # function_call_response = result.parts[0].function_response.response
                    # print(f"-> {function_call_response}")
            else:
                is_functions_finished = True
                print("response: ", response.text)

                if is_verbose:  
                    print("User prompt:", user_prompt)
                    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                    print("Response tokens:", response.usage_metadata.candidates_token_count)
    except Exception as e:
        print("unexpected error: ", e)

def gen_content(system_prompt, client, contents, model):
    response = client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions]
            )
        )
    
    return response

########### Functions called in main program ###########

def get_api_key():
    try:
        load_dotenv()
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        if gemini_api_key == None:
            raise ValueError("gemini_api_key evaluated to blank value")
        return gemini_api_key
    except Exception as e:
        print("error occured when trying to get gemini_api_key: ", e)
        exit(1)


def get_arg_from_user():
    try:
        prompt = get_arg_from_sys_argv()
        return prompt
    except Exception as e:
        print("error occured when trying to get prompt: ", e)
        exit(1)

if __name__ == "__main__":
    main()
