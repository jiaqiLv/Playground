import base64
import urllib
import requests
import urllib.parse

# API_KEY = "CnVVzJDBvTcUOVYLJc5fTAv0"
# SECRET_KEY = "ieBih03MxboSHV9whzU33Gpk5TOrrkJQ"

API_KEY = "7SAjqMH99A9Ko9BAvIX5UYtC"
SECRET_KEY = "jie5MFcAeIoaaA5s2MLhfvleSmbyDNaN"


def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content

def get_access_token():
    """
    使用 AK,SK 生成鉴权签名(Access Token)
    :return: access_token,或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

def load_code(file_path):
    with open(file_path,'r') as file:
        code = file.read()
    # code = code.split('image')[-1]
    return code

def generate_by_base64(code, save_path, urlencoded=False):
    if urlencoded:
        code = urllib.parse.unquote_plus(code)
    image_data = base64.b64decode(code)
    with open(save_path, "wb") as f:
        f.write(image_data)

if __name__ == '__main__':
    code = load_code('./code.txt')
    generate_by_base64(code,'./save_image.png',False)