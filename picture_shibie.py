import requests
import base64
import re
import json

def has_english(s):
    # 匹配任意英文字母（大小写）
    return bool(re.search(r'[a-zA-Z]', s))

def is_all_digits(s):
    # 匹配从头到尾都是数字的字符串（空字符串返回False）
    return bool(re.fullmatch(r'\d+', s))

def get_pic_word(pic_path, API_KEY, SECRET_KEY):
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + get_access_token(API_KEY, SECRET_KEY)

    f = open(pic_path, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img}

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=params)
    data_list = json.loads(response.text)['words_result']
    result_word = ""
    for data in data_list:
        word = data['words']
        if not has_english(word) and not is_all_digits(word):
            result_word += (word + ",")
    print(result_word[:-1])
    return result_word[:-1]


def get_access_token(API_KEY, SECRET_KEY):
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
