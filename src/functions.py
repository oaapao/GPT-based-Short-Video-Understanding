# -- coding:utf-8 --
from src.utils.speech2text import speech_to_text
from src.utils.video2speech import video_to_speech

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
