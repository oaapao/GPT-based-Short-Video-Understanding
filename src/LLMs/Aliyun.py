from http import HTTPStatus
from dashscope import Generation


def chat_with_qwen(content, system='你是ChatGPT'):
    messages = [{'role': 'system', 'content': system},
                {'role': 'user', 'content': content}]
    gen = Generation()
    response = gen.call(
        Generation.Models.qwen_v1,
        messages=messages,
        result_format='message', # set the result is message format.
    )
    if response.status_code == HTTPStatus.OK:   
        return response.output.choices[0].message.content
    else:
        return 'Request id: %s, Status code: %s, error code: %s, error message: %s'%(
            response.request_id, response.status_code, 
            response.code, response.message
        )  

if __name__ == '__main__':
    chat = '你好'
    res = chat_with_qwen(chat)
    print(res)