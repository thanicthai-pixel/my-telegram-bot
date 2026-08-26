import os
import random
import requests
from fastapi import FastAPI
from PIL import Image, ImageDraw, ImageFont

# สร้างแอป FastAPI ( Render ต้องการตัวแปร app นี้ครับ )
app = FastAPI()

# 🔑 ใส่ BOT_TOKEN และ CHAT_ID ของคุณตรงนี้
BOT_TOKEN ="8825722253:AAFIyG1d6US4XOkbsoI55SzkREYRZblNgEI"
CHAT_ID = "1880260879"

@app.get("/")
def home():
    return {"status": "Bot is running"}

@app.get("/send-lottery")
def send_lottery():
    # 1. สุ่มตัวเลข 2 ชุด (บน-ล่าง) และเลขวิ่ง 1 ตัว
    set1 = f"{random.randint(0, 99):02d}"
    set2 = f"{random.randint(0, 99):02d}"
    running_num = f"{random.randint(0, 9)}"

    # 2. เปิดรูปภาพ Template
    img_path = "ves_template.jpg"
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size

    # 3. โหลดฟอนต์ระบบ
    try:
        font_main = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
        font_sub = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # 4. กำหนดข้อความ
    text_main = f"{set1} - {set2}"
    text_sub = f"วิ่ง {running_num}"

    # 5. จัดวางตำแหน่งให้อยู่กึ่งกลางภาพพอดี
    bbox1 = draw.textbbox((0, 0), text_main, font=font_main)
    w1 = bbox1[2] - bbox1[0]
    x1 = max(0, (img_width - w1) / 2)
    y1 = max(10, (img_height / 2) - 50)

    bbox2 = draw.textbbox((0, 0), text_sub, font=font_sub)
    w2 = bbox2[2] - bbox2[0]
    x2 = max(0, (img_width - w2) / 2)
    y2 = y1 + 70

    # 6. วาดตัวหนังสือบนภาพ (สีเขียวเข้ม และ สีทอง)
    draw.text((x1, y1), text_main, fill="#053B18", font=font_main)
    draw.text((x2, y2), text_sub, fill="#C59B27", font=font_sub)

    # 7. บันทึกรูปภาพ
    output_path = "output.jpg"
    img.save(output_path)

    # 8. ส่งภาพเข้า Telegram
    caption = "งวดนี้รวย! ไม่รวยงวดนี้ จะไปรวยงวดไหน!🍀"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    
    with open(output_path, "rb") as photo:
        payload = {"chat_id": CHAT_ID, "caption": caption}
        files = {"photo": photo}
        res = requests.post(url, data=payload, files=files)

    return {"status": "success", "telegram_response": res.json()}
