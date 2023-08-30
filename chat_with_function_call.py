# -- coding:utf-8 --
import logging
import os
from src.functions import functions, available_functions
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
    video_path = 'data/examples/真实车主吐槽吉利银河L7，一起来看看有没有你在意的点.mp4'
    prompt = f"""
    你是一个智能机器人，必要时可以调用我给你提供的外部工具，请你尽可能执行下面操作：
    1. 将视频“{video_path}”中的语音分离出来，并将语音转成文字，结合视频的标题和转化的文字生成该视频的主题；
    2. 结合视频的标题，对识别出的文字按照标签进行分类，比如质量缺陷（发动机、车身、传动系统等）、品牌口碑、汽车需求相关（动力、底盘、座舱、车身、自动驾驶等）、汽车服务相关（销售欺诈、服务态度、服务收费等），
    例如，如果有部分视频表达了“实体按键缺失”或“车内空间利用不佳”这种不影响实际功能，但影响用户体验的则应该被分为“汽车需求相关”；
    如果有部分视频表达了“刹车经常失灵”或“发动机动力不足”这种影响实际驾驶的应该被分类为“质量缺陷”；
    如果有部分视频表达了“某某品牌的车好”或“某某品牌的车很不好”这种对品牌的评价，应该被分类为“品牌口碑”；
    如果有部分视频表达了对销售人员或客服人员或售后服务的评价，则应该被分类为“汽车服务相关”。
    请注意：由于我们提供的音频转文字的外部接口准确性有限，因此可能会导致个别词语或句子转化错误，你可以根据其发音在全文语境下进行联想和整体分析。

    下面给你一个回答的示例，请你严格按照这个例子的格式输出你的最终回答：
    视频主题：XXXXXXXXXXXXXX
    视频内容分析和分类结果：
    1. 质量缺陷：指出视频中提到了哪些质量缺陷，用“；”符号分割开，没有的话写“未提及”
    2. 品牌口碑：指出视频中提到了哪些品牌口碑，用“；”符号分割开，没有的话写“未提及”
    3. 汽车服务相关：指出视频中提到了哪些汽车服务相关，用“；”符号分割开，没有的话写“未提及”
    4. 汽车需求相关：指出视频中提到了哪些汽车需求相关，用“；”符号分割开，没有的话写“未提及”
    """
    res = chat_with_functions(prompt)
    print(res)
    
