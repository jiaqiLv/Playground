import base64
import urllib
import requests
from utils import (get_file_content_as_base64,
                   get_access_token,
                   generate_by_base64,
                   create_pdf_with_image_text)
import logging
import json
import cv2
import win32print
import win32ui
import win32api
from PIL import Image,ImageWin
import os
import qianfan

os.environ["QIANFAN_ACCESS_KEY"] = "c09abdfc9d9c4ac2af18e23ab8c77788"
os.environ["QIANFAN_SECRET_KEY"] = "06020355ca7947528f15a6965d695a2e"

# 配置基本的日志设置
logging.basicConfig(level=logging.DEBUG,  # 设置日志级别
                    format='%(asctime)s - %(levelname)s - %(message)s',  # 设置日志格式
                    datefmt='%Y-%m-%d %H:%M:%S',  # 设置日期时间格式
                    filename='./log.log',  # 设置日志文件名（如果不写就是输出到控制台）
                    filemode='w')  # 设置写入模式为“写入”（'w'）或“追加”（'a'）

def image_recognition(image_path):
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/plant?access_token=" + get_access_token(application_type="image_recognition")
    # image 可以通过 get_file_content_as_base64("C:\fakepath\maple.jpg",True) 方法获取
    image = get_file_content_as_base64(image_path,True)
    payload = f'image={image}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    highest_score_item = max(data["result"], key=lambda x: x["score"])
    name_with_highest_score = highest_score_item["name"]
    print('Object class:', name_with_highest_score)
    return name_with_highest_score

def style_generation(image_path,save_path,option='wave'):
    """
    cartoon：卡通画风格
    pencil：铅笔风格
    color_pencil：彩色铅笔画风格
    warm：彩色糖块油画风格
    wave：神奈川冲浪里油画风格
    lavender：薰衣草油画风格
    mononoke：奇异油画风格
    scream：呐喊油画风格
    gothic：哥特油画风格
    """
    url = "https://aip.baidubce.com/rest/2.0/image-process/v1/style_trans?access_token=" + get_access_token(application_type="style_generation")
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

def description(object_class):
    chat_comp = qianfan.ChatCompletion()
    resp = chat_comp.do(model="ERNIE-4.0-8K-Latest", messages=[{
        "role": "user",
        "content": f"请给出下面植物的百度百科词条描述信息，字数限制在150字以内：{object_class}"
    }])
    print(resp["body"])
    return resp["body"]['result']

def shooting():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('Unable to turn on the camera.')
        exit(-1)

    image_path = 'captured_photo.jpg'
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Captured Image', frame)
        else:
            print("Unable to capture image.")
        
        key = cv2.waitKey(1)
        if key == ord('k'):
            cv2.imwrite(image_path, frame)
            print(f"Save photo at {image_path}")
            cap.release()
            cv2.destroyAllWindows()
            break
    return image_path

def printer_pdf(pdf_path):
    printer_name = win32print.GetDefaultPrinter()
    win32api.ShellExecute(0,'print',pdf_path,None,'.',0)

def printer(image_path):
    image = Image.open(image_path)
    printer_name = win32print.GetDefaultPrinter()
    hprinter = win32print.OpenPrinter(printer_name)
    try:
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)
        hdc.StartDoc(image_path)
        hdc.StartPage()
        dib = ImageWin.Dib(image)
        dib.draw(hdc.GetHandleOutput(), (0, 0, image.size[0], image.size[1]))
        hdc.EndPage()
        hdc.EndDoc()
    finally:
        win32print.ClosePrinter(hprinter)

def main():
    save_path = './photo.png'
    pdf_path = './output.pdf'
    image_path = './flower.jpg'
    # image_path = shooting()
    object_class = image_recognition(image_path)
    text = description(object_class=object_class)
    print(text)
    style_generation(image_path,save_path=save_path)
    create_pdf_with_image_text(pdf_path,save_path,text)
    # printer_pdf(pdf_path)

if __name__ == '__main__':
    main()
