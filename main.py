#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pprint import pprint
from argument_parsing import get_arg_from_sys_argv
from loading import load_binary

def main():
    gemini_api_key = get_api_key()
    # print("gemini_api_key: ", gemini_api_key)
    client = genai.Client(api_key=gemini_api_key)
    
    # prompt = types.Part.from_text(text=get_arg_from_user())
    text_part = types.Part.from_text(text="What is actually being shown in this image")

    image = load_binary("./test_dog.jpg")
    image_part = types.Part.from_bytes(data=image, mime_type="image/jpeg")
    content  = types.Content(role="user", parts=[text_part,
                                                image_part
                                                ])

    model = "gemini-2.0-flash-001"

    response = client.models.generate_content(
        model=model,
        contents=[content]
    )
    print("response: ", response.text)
    print("##### usage metadata #####")
    pprint(response.usage_metadata.__dict__)

    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)


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
