import io
import cv2
import numpy as np
import qrcode
from fastapi import UploadFile

# 加载QRCode检测器模型
detector = cv2.wechat_qrcode_WeChatQRCode(
    "core_models/wechat_qrcode/detect.prototxt",
    "core_models/wechat_qrcode/detect.caffemodel",
    "core_models/wechat_qrcode/sr.prototxt",
    "core_models/wechat_qrcode/sr.caffemodel"
)

def generate_qrcode_image(text: str) -> io.BytesIO:
    """生成二维码并返回内存二进制数据流"""
    img_buffer = io.BytesIO()
    img = qrcode.make(text)
    img.save(img_buffer, "PNG")
    img_buffer.seek(0)
    return img_buffer

async def decode_qrcode_from_image(file: UploadFile) -> list:
    """读取上传图片并解码"""
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    # 返回解码的文本列表
    res, _ = detector.detectAndDecode(image)
    return res