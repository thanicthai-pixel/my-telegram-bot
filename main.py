import os
import random
import requests
from fastapi import FastAPI
from PIL import Image, ImageDraw, ImageFont

app = FastAPI()

# 🔑 กำหนดค่า TOKEN และ CHAT_ID ตรงนี้
BOT_TOKEN = "8825722253:AAEFqblufxTK1bqRasup2FmlC2VfVexOzgU"
CHAT_ID = "1880260879"

@app.get("/")
def home():
    return {"status": "Bot is running"}

@app.get("/send-lottery")
def send_lottery():
    # 1. สุ่มตัวเลข
    set1 = f"{random.randint(0, 99):02d}"
    set2 = f"{random.randint(0, 99):02d}"
    running_num = f"{random.randint(0, 9)}"

    # 2. เปิดรูป Template
    img_path = "ves_template.jpg"
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size

    # 3. โหลดฟอนต์ระบบ DejaVuSans ตัวหนา
    try:
        font_main = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
        font_sub = ImageFont.truetype("DejaVuSans-Bold.ttf", 55)
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # 4. กำหนดข้อความ (ใช้ Run : แทน วิ่ง เพื่อเลี่ยงปัญหาสี่เหลี่ยมฟอนต์ระบบ)
    text_main = f"{set1} - {set2}"
    text_sub = f"Run : {running_num}"

    # 5. คำนวณตำแหน่งกึ่งกลาง
    bbox1 = draw.textbbox((0, 0), text_main, font=font_main)
    w1 = bbox1[2] - bbox1[0]
    x1 = max(0, (img_width - w1) / 2)
    y1 = max(10, (img_height / 2) - 75)

    bbox2 = draw.textbbox((0, 0), text_sub, font=font_sub)
    w2 = bbox2[2] - bbox2[0]
    x2 = max(0, (img_width - w2) / 2)
    y2 = y1 + 100

    # 6. เทคนิคสร้างตัวหนังสือสีทองขอบเข้มหนา (Stroke Multi-layer เพิ่มมิติความเด่น)
    # วาดขอบเงาหนาด้านหลัง
    draw.text((x1+2, y1+2), text_main, font=font_main, fill="#1A0D00", stroke_width=7, stroke_fill="#1A0D00")
    draw.text((x1, y1), text_main, font=font_main, fill="#2B1400", stroke_width=4, stroke_fill="#2B1400")
    # วาดตัวอักษรสีทองสว่างทับด้านบน
    draw.text((x1, y1), text_main, font=font_main, fill="#FFD700")

    # บรรทัดเลขวิ่ง
    draw.text((x2+2, y2+2), text_sub, font=font_sub, fill="#1A0D00", stroke_width=6, stroke_fill="#1A0D00")
    draw.text((x2, y2), text_sub, font=font_sub, fill="#2B1400", stroke_width=4, stroke_fill="#2B1400")
    draw.text((x2, y2), text_sub, font=font_sub, fill="#FF8C00") # สีทองส้มเด่นๆ

    # 7. บันทึกและส่งภาพ
    output_path = "output.jpg"
    img.save(output_path)

    caption = "งวดนี้รวย! ไม่รวยงวดนี้ จะไปรวยงวดไหน!🍀"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    
    with open(output_path, "rb") as photo:
        payload = {"chat_id": CHAT_ID, "caption": caption}
        files = {"photo": photo}
        res = requests.post(url, data=payload, files=files)

    return {"status": "success", "telegram_response": res.json()}
