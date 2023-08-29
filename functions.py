# -- coding:utf-8 --
from pprint import pprint
import requests
from speech2text import speech_to_text
from video2speech import video_to_speech

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Dnt": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
    "X-Amzn-Trace-Id": "Root=1-64e46c6e-04a7c5d33c1530af0214cffc",
}


functions = [
    {
        "name": "video_to_speech",
        "description": "将本地的视频文件转化为音频文件，如果操作成功则返回ok",
        "parameters": {
            "type": "object",
            "properties": {
                "video_filename": {
                    "type": "string",
                    "description": "待转化的视频文件",
                },
                "wav_filename": {
                    "type": "string",
                    "description": "输出的音频文件保存路径，请你存放在data/examples文件夹中，例如data/examples/abc.wav",
                }
            },
            "required": ["video_filename","wav_filename"],
        },
    },
     {
        "name": "speech_to_text",
        "description": "将本地的音频文件转化为对应的文本或文字，如果成功则返回转化后的文本或文字",
        "parameters": {
            "type": "object",
            "properties": {
                "audio_filename": {
                    "type": "string",
                    "description": "待转化的本地音频文件",
                },
            },
            "required": ["audio_filename"],
        },
    },
]

available_functions = {
    "video_to_speech": video_to_speech,
    "speech_to_text":speech_to_text

}
