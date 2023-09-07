from src.LLMs.Baidu import chat_with_wenyan
from src.LLMs.Xunfei import chat_with_spark


def get_llm(name):
    # 百度出品的大模型
    if name == 'Baidu' or name == 'baidu' or name == 'wenxin':
        return chat_with_wenyan
    # 讯飞出品的大模型
    if name == 'Xunfei'or name == 'xunfei' or name == 'spark':
        return chat_with_spark
    else:
        raise RuntimeError('Not supported LLM')