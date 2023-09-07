import time
import os

from tqdm import tqdm
from src.LLMs.api import get_llm

from src.utils.save_text import save_text_to_txt
from src.utils.speech2text import speech_to_text
from src.utils.video2speech import video_to_speech
from src.utils.summarize import summary_to_csv

    
def batch_process(llm='Baidu', sec_uid='MS4wLjABAAAANDIHLwHtMrXJ5vukUYqhujOLhdBBkJg5qg__R9pb_Q4'):
    chat_with_llm = get_llm(llm)
    # sec_uid = 'test'
    video_dir = f'data/{sec_uid}/'  # 爬取到的视频目录
    files = [i for i in os.listdir(video_dir) if i.endswith('.mp4')]

    for video_name in tqdm(files):
        # video_name = '22款福特猛禽车主被外观征服 #福特猛禽 #猛禽 #福特 #皮卡 #车主说 #长城炮.mp4'
        video_prefix = video_name[0:-4]
        
        # 百度,星火等GPT不支持Function call 因此需要hard code预处理步骤
        video_to_speech(video_dir+video_name,video_dir+video_prefix+f'-{llm}.wav')
        text = speech_to_text(video_dir+video_prefix+f'-{llm}.wav')
        save_text_to_txt(text,video_dir+video_prefix+f'-{llm}.txt')

        prompt = f"""
        你是一个短视频汽车领域的专家，擅长解决视频舆情分析任务;
        给你从视频“{video_name}”提取到的对应文字：
        “{text}”
        
        请你：
        1. 结合视频的标题和转化的文字生成该视频的主题（主题不超过十五个字），并分析视频主要内容（需要使用第三人称，语言凝练、抓重点）；
        1. 分析视频包含了哪些关键内容，包括：质量缺陷（发动机、车身、传动系统等）、品牌口碑、汽车需求相关（动力、底盘、座舱、车身、自动驾驶等）、汽车服务相关（销售欺诈、服务态度、服务收费等）
        
        下面给你一个回答的示例，请你根据视频文字内容、严格按照这个例子的格式输出你的最终回答：
        视频主题:XXXXXX
        视频主要内容:XXXXXXXXXXXXXXXXXXXXXXXXXX
        质量缺陷:XXX,XXX (描述影响汽车实际驾驶的、危害安全的问题，例如“发动机动力不足”，用“,”符号分割开，没有的话写“未提及”)
        品牌口碑:XXX,XXX (描述正向或负向的关于品牌的口碑的内容，例如“本田思域很好”，用“,”符号分割开，没有的话写“未提及”)
        汽车服务相关:XXX,XXX (描述对销售人员或售后服务的评价的内容，例如“售后不行”，用“,”符号分割开，没有的话写“未提及”)
        汽车需求相关:XXX,XXX,XXX (描述能提升驾驶体验的内容，以及除了“质量缺陷”以外的所有问题和建议，用“,”符号分割开，没有的话写“未提及”)
        """
        res = chat_with_llm(prompt)
        save_text_to_txt(res, video_dir+f'{llm}-'+video_prefix+'.txt')
        time.sleep(1)

    summary_to_csv(llm, sec_uid)


if __name__ == '__main__':
    batch_process('Xunfei')