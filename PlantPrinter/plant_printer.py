import base64
import urllib
import requests
from utils import (get_file_content_as_base64,
                   get_access_token,
                   generate_by_base64)
import logging
import json
import cv2
import win32print
import win32ui
from PIL import Image,ImageWin

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
    save_path = './sunflower_gen.png'
    image_path = shooting()
    style_generation(image_path,save_path=save_path)
    printer(save_path)

if __name__ == '__main__':
    main()
