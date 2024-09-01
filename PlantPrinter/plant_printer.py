import base64
import urllib
import requests
from utils import (get_file_content_as_base64,
                   get_access_token,
                   generate_by_base64)
import logging
import json

# 配置基本的日志设置
logging.basicConfig(level=logging.DEBUG,  # 设置日志级别
                    format='%(asctime)s - %(levelname)s - %(message)s',  # 设置日志格式
                    datefmt='%Y-%m-%d %H:%M:%S',  # 设置日期时间格式
                    filename='./log.log',  # 设置日志文件名（如果不写就是输出到控制台）
                    filemode='w')  # 设置写入模式为“写入”（'w'）或“追加”（'a'）

def image_recognition(image_path):
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/plant?access_token=" + get_access_token()
    # image 可以通过 get_file_content_as_base64("C:\fakepath\maple.jpg",True) 方法获取
    image = get_file_content_as_base64(image_path,True)
    payload = f'image={image}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def style_generation(image_path,save_path,option='pencil'):
    url = "https://aip.baidubce.com/rest/2.0/image-process/v1/style_trans?access_token=" + get_access_token()
    image = get_file_content_as_base64(image_path,True)
    payload = f'option={option}&image={image}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    logging.info(response.text)
    code = json.loads(response.text)["image"]
    generate_by_base64(code,save_path)
    print('Success! Image saved at {}'.format(save_path))

def main():
    style_generation('./sunflower.jpg','./sunflower_gen.png')

if __name__ == '__main__':
    main()
