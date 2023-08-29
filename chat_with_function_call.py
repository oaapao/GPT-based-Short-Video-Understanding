# -- coding:utf-8 --
import logging
import os
from functions import functions, available_functions
import openai
import json
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type
)  # for exponential backoff

logging.basicConfig(level=logging.INFO)

openai.api_key = os.getenv("CHATGPT_AK")


@retry(retry=retry_if_exception_type((openai.error.APIError, openai.error.APIConnectionError, openai.error.RateLimitError, openai.error.ServiceUnavailableError, openai.error.Timeout)), wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_attempt(10))
def chat_completion_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)


def chat_with_functions(content):
    messages = [{"role": "user", "content": content}]
    first_response = chat_completion_with_backoff(
        model='gpt-3.5-turbo-0613',
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    response_message = first_response["choices"][0]["message"]

    while response_message.get("function_call"):
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        # print(response_message["function_call"]["arguments"])
        
        function_args = json.loads(response_message["function_call"]["arguments"], strict=False)
        logging.info(f"Calling {function_name}")
        function_response = fuction_to_call(**function_args)

        messages.append(
            {
                "role": response_message["role"],
                "function_call": {
                    "name": response_message["function_call"]["name"],
                    "arguments": response_message["function_call"]["arguments"],
                },
                "content": None,
            }
        )
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )

        response = chat_completion_with_backoff(
            model='gpt-3.5-turbo-0613',
            messages=messages,
            functions=functions,
            function_call="auto",
        )
        response_message = response["choices"][0]["message"]
    
    return response_message["content"]


if __name__ == "__main__":
    prompt = """
    请你将视频文件sample.mp4转化为文本，然后分析情感，从“好评”、“一般”，“差评”中选择最合适的情感评价，并给出原因。
    请注意：1. 由于我们提供的音频转文字的外部接口准确性有限，因此可能会导致个别词语或句子转化错误，你可以根据其发音在全文语境下进行联想和整体分析； 2. 在回答的最后另起一行给出两个字的回答，例如“好评”。
    """
    res = chat_with_functions(prompt)
    print(res)
    
