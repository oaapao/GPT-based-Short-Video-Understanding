# -- coding:utf-8 --
import logging
import os
import time

from tqdm import tqdm
from src.functions import functions, available_functions
import openai
import json
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type
)

from src.utils.save_text import save_text_to_txt
from summarize import summary_to_csv

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

def batch_process(sec_uid='MS4wLjABAAAANDIHLwHtMrXJ5vukUYqhujOLhdBBkJg5qg__R9pb_Q4'):
    # sec_uid = 'test'
    video_dir = f'data/{sec_uid}/'  # 爬取到的视频目录
    files = [i for i in os.listdir(video_dir) if i.endswith('.mp4')][15:]

    for video_name in tqdm(files):
        # video_name = '22款福特猛禽车主被外观征服 #福特猛禽 #猛禽 #福特 #皮卡 #车主说 #长城炮.mp4'
        video_prefix = video_name[0:-4]
        prompt = f"""
        你是一个短视频汽车领域的专家，擅长使用外部工具解决视频舆情分析任务，请你尽可能执行下面操作：
        1. 将视频“{video_dir}{video_name}”中的语音分离出来，并将语音转成文字，将文字保存到“{video_dir}{video_prefix}.txt”；
        2. 结合视频的标题和转化的文字生成该视频的主题（主题不超过十五个字），并分析视频主要内容（需要使用第三人称，语言凝练、抓重点）；
        3. 分析视频包含了哪些关键内容，包括：质量缺陷（发动机、车身、传动系统等）、品牌口碑、汽车需求相关（动力、底盘、座舱、车身、自动驾驶等）、汽车服务相关（销售欺诈、服务态度、服务收费等）
        
        下面给你一个回答的示例，请你根据视频文字内容、严格按照这个例子的格式输出你的最终回答：
        视频主题:XXXXXX
        视频主要内容:XXXXXXXXXXXXXXXXXXXXXXXXXX
        质量缺陷:XXX,XXX (描述影响汽车实际驾驶的、危害安全的问题，例如“发动机动力不足”，用“,”符号分割开，没有的话写“未提及”)
        品牌口碑:XXX,XXX (描述正向或负向的关于品牌的口碑的内容，例如“本田思域很好”，用“,”符号分割开，没有的话写“未提及”)
        汽车服务相关:XXX,XXX (描述对销售人员或售后服务的评价的内容，例如“售后不行”，用“,”符号分割开，没有的话写“未提及”)
        汽车需求相关:XXX,XXX,XXX (描述能提升驾驶体验的内容，以及除了“质量缺陷”以外的所有问题和建议，用“,”符号分割开，没有的话写“未提及”)
        """
        res = chat_with_functions(prompt)
        save_text_to_txt(res, video_dir+'gpt-'+video_prefix+'.txt')
        time.sleep(2)

    summary_to_csv(sec_uid)


if __name__ == "__main__":
    sec_uid='MS4wLjABAAAANDIHLwHtMrXJ5vukUYqhujOLhdBBkJg5qg__R9pb_Q4'
    batch_process(sec_uid=sec_uid)
    