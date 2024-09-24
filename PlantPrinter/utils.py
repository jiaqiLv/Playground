import base64
import urllib
import requests
import urllib.parse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

# API_KEY = "CnVVzJDBvTcUOVYLJc5fTAv0"
# SECRET_KEY = "ieBih03MxboSHV9whzU33Gpk5TOrrkJQ"

# API_KEY = "7SAjqMH99A9Ko9BAvIX5UYtC"
# SECRET_KEY = "jie5MFcAeIoaaA5s2MLhfvleSmbyDNaN"


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

def get_access_token(application_type='style_generation'):
    """
    使用 AK,SK 生成鉴权签名(Access Token)
    :return: access_token,或是None(如果错误)
    """
    if application_type == 'style_generation':
        API_KEY = "7SAjqMH99A9Ko9BAvIX5UYtC"
        SECRET_KEY = "jie5MFcAeIoaaA5s2MLhfvleSmbyDNaN"
    elif application_type == 'image_recognition':
        API_KEY = "CnVVzJDBvTcUOVYLJc5fTAv0"
        SECRET_KEY = "ieBih03MxboSHV9whzU33Gpk5TOrrkJQ"

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

def create_pdf_with_image_text(pdf_path, image_path, text):
    pdfmetrics.registerFont(TTFont('SimSun', 'SimSun.ttf'))  # 确保将字体文件放在当前目录
    # 创建一个PDF画布，指定A4页面大小
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    # 添加图像
    img = Image.open(image_path)
    img_width, img_height = img.size
    # 根据A4纸的尺寸对图像进行缩放
    max_width = width - 50  # 保留一定的边距
    max_height = height / 2  # 图像占用半页
    if img_width > max_width or img_height > max_height:
        scaling_factor = min(max_width / img_width, max_height / img_height)
        img_width = img_width * scaling_factor
        img_height = img_height * scaling_factor
    # 在A4纸上放置图像，位置在页面顶部
    c.drawImage(image_path, 25, height - img_height - 25, img_width, img_height)
    # 添加文本，位置在页面的图像下方
    text_y_position = height - img_height - 50  # 文本开始的y坐标
    c.setFont("Helvetica", 12)
    text_lines = text.split('\n')
    for line in text_lines:
        c.setFont("SimSun", 12)
        c.drawString(25, text_y_position, line)
        text_y_position -= 15  # 每行文本向下移15个单位
    # 保存PDF文件
    c.save()

if __name__ == '__main__':
    text = 'Hello! 你好！'
    image_path = './photo.png'
    create_pdf_with_image_text('./test.pdf',image_path,text)
    # code = load_code('./code.txt')
    # generate_by_base64(code,'./save_image.png',False)