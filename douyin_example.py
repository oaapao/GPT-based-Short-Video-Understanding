import json
from pprint import pprint
import requests
import asyncio
from tikhub import DouyinAPI

def phase_id_and_share_url(json_filename='./search_result.json'):
    with open(json_filename,'r') as f:
        data = json.load(f)
    share_list = []
    for i in data['data']:
        total_url = i['aweme_info']['share_info']['share_url']
        share_list.append((i['aweme_info']['aweme_id'], total_url[0:int(total_url.index("&"))]))
    return share_list

def download_douyin(save_path,share_url=None,vid=None):
    

    token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjExOTMyMjc1NTFAcXEuY29tIiwiZXhwIjoxNzI0NzcwNzUzLCJlbWFpbCI6IjExOTMyMjc1NTFAcXEuY29tIiwiZXZpbDEiOiIkMmIkMTIkM0RHVHcuQTJBTzF1SzdaV0QvUE5MLkNsV3RlOGpCRS93SHNUUGdZdkgvcnFibWNrNXp0bGkifQ.l6bp4K53aclCWXM_fBnKHSAmPeGhILqo12AOcyBCByo"
    douyin_api = DouyinAPI(token)

    r = None
    r = asyncio.run(douyin_api.get_douyin_video_data(video_id=vid))
    download_url = r['aweme_list'][0]['video']['play_addr']['url_list'][0]
    
    r = requests.get(download_url)
    with open(save_path,'wb') as f:
        f.write(r.content)
        f.close()


if __name__ == '__main__':
    # pprint(phase_id_and_share_url())
    res = download_douyin(save_path='sample.mp4',vid='7271122752621301026')