import json
import os
from pprint import pprint
import requests
import asyncio
from tikhub import DouyinAPI
from tqdm import tqdm

# token每天有次数限制
token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjUzMDI4ODk2N0BxcS5jb20iLCJleHAiOjE3MjU0MTE5MTAsImVtYWlsIjoiNTMwMjg4OTY3QHFxLmNvbSIsImV2aWwxIjoiJDJiJDEyJGRTT1RWUkkxRVBjb3VaalY4SHd0cWVmNlguWlhxZUlBVlpmWEVWVUJ6b0wwV1Exano1MTNHIn0.dloXptkfisvwgvcpVH0efAq5qoZnyNl7JswUtK0WFEo"
douyin_api = DouyinAPI(token)

def phase_id_and_share_url(json_filename='./search_result.json'):
    """根据抖音搜索接口的响应的json，解析搜索结果中视频数据的ID和分享链接

    Args:
        json_filename (str, optional): 抖音搜索接口的响应json. Defaults to './search_result.json'.
        1. open https://www.douyin.com/ in browser
        2. press F12 and seletct Network to record the requests and responses
        3. search video data by some keyword
        4. select the request url with https://www.douyin.com/aweme/v1/web/search/item/?device_platform=webapp...
        5. save the json response the ./search_result.json
    Returns:
        List[turple]: a list of pairs of video id and share list
    """
    with open(json_filename,'r') as f:
        data = json.load(f)
    share_list = []
    for i in data['data']:
        total_url = i['aweme_info']['share_info']['share_url']
        share_list.append((i['aweme_info']['aweme_id'], total_url[0:int(total_url.index("&"))]))
    return share_list

def download_douyin(save_path,share_url=None,vid=None):
    """调用抖音非官方接口(https://github.com/TikHubIO/Douyin-TikTok-API-Python-SDK)，
    根据视频链接或ID下载原视频

    Args:
        save_path (string): 保存路径
        share_url (string, optional): 视频的分享链接. Defaults to None.
        vid (_type_, optional): 视频的ID. Defaults to None.
    """
    
    try:
        r = None
        r = asyncio.run(douyin_api.get_douyin_user_profile_videos_data())
        r = asyncio.run(douyin_api.get_douyin_video_data(video_id=vid))
        download_url = r['aweme_list'][0]['video']['play_addr']['url_list'][0]
        
        r = requests.get(download_url)
        with open(save_path,'wb') as f:
            f.write(r.content)
            f.close()
        return 'ok'
    except Exception as e:
        return f'Download failed with error message: {e.__str__}'
    

def download_douyin_user_all_video(sec_uid='MS4wLjABAAAANDIHLwHtMrXJ5vukUYqhujOLhdBBkJg5qg__R9pb_Q4'):
    # 调用第三方服务爬取抖音视频
    r = None
    # r = asyncio.run(douyin_api.get_douyin_user_profile_videos_data(sec_user_id=sec_uid,count=50))
    r = asyncio.run(douyin_api.get_douyin_user_profile_videos_data(sec_user_id=sec_uid,count=50))
    
    urls = []
    titles = []
    for info in r['aweme_list']:
        urls.append(info['video']['play_addr']['url_list'][0])
        titles.append(info['preview_title'])
    for i in tqdm(range(len(urls))):
        r = requests.get(urls[i])
        if not os.path.exists(f'data/{sec_uid}'):
            os.mkdir(f'data/{sec_uid}')
        with open((f'data/{sec_uid}/{titles[i]}.mp4'),'wb') as f:
            f.write(r.content)
            f.close()



if __name__ == '__main__':
    # pprint(phase_id_and_share_url())
    # res = download_douyin(save_path='sample1.mp4',vid='7271122752621301026')
    # download_douyin_user_all_video()
    download_douyin_user_all_video()