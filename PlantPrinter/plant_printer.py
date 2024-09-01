
# encoding:utf-8

import requests
import base64

'''
植物识别
'''

if __name__ == '__main__':
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/plant"
    # 二进制方式打开图片文件
    f = open('./maple.jpg', 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    access_token = 'dNiLrq21KhEOIbrcvregCzsk'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print (response.json())