import requests
import json
import os


wenxin_ak = os.getenv("BAIDU_WENXIN_AK")
wenxin_sk = os.getenv("BAIDU_WENXIN_SK")

def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """        
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={wenxin_ak}&client_secret={wenxin_sk}"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def chat_with_wenyan(content):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": content
            },
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    json_res = json.loads(response.text)
    return json_res['result']