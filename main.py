import os
import random
import requests
from fastapi import FastAPI
from PIL import Image, ImageDraw, ImageFont

app = FastAPI()

BOT_TOKEN = "8825722253:AAflyG1d6US4XOkbsoI55SzkREYZbINgEI"
CHAT_ID = "1880260879"

# ฟังก์ชันโหลดฟอนต์ไทยสวยๆ (ดึงจาก Google Fonts อัตโนมัติถ้าไม่มีไฟล์)
def get_thai_font(size):
    font_filename = "Prompt-Bold.ttf"
    if not os.path.exists(font_filename):
        # โหลดฟอนต์ Prompt Bold จาก Google Fonts GitHub
        font_url = "https://github.com/google/fonts/raw/main/ofl/prompt/Prompt-Bold.ttf"
        try:
            r = requests.get(font_url)
            with open(font_filename, "wb") as f:
                f.write(r.content)
        except:
            pass
            
    try:
        return ImageFont.truetype(font_filename, size)
    except:
        return ImageFont.load_default()

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

    # 3. โหลดฟอนต์ขนาดใหญ่พิเศษ
    font_main = get_thai_font(85)  # ขนาดเลขบน-ล่าง
    font_sub = get_thai_font(65)   # ขนาดเลขวิ่ง

    # 4. ข้อความที่จะแสดงผล
    text_main = f"{set1} - {set2}"
    text_sub = f"วิ่ง {running_num}"

    # 5. จัดตำแหน่งกึ่งกลางภาพ
    bbox1 = draw.textbbox((0, 0), text_main, font=font_main)
    w1 = bbox1[2] - bbox1[0]
    x1 = max(0, (img_width - w1) / 2)
    y1 = max(10, (img_height / 2) - 80)

    bbox2 = draw.textbbox((0, 0), text_sub, font=font_sub)
    w2 = bbox2[2] - bbox2[0]
    x2 = max(0, (img_width - w2) / 2)
    y2 = y1 + 105

    # 6. วาดข้อความพร้อมขอบเงาหนา (Outline / Stroke) ให้ตัวอักษรเด่นและมีมิติ
    # -- วาดบรรทัดที่ 1 (เลข 2 ชุด) --
    draw.text((x1, y1), text_main, font=font_main, fill="#4A2500", stroke_width=4, stroke_fill="#2B1400") # เงา/ขอบเข้ม
    draw.text((x1, y1), text_main, font=font_main, fill="#FFD700") # ตัวอักษรสีทองสว่าง

    # -- วาดบรรทัดที่ 2 (เลขวิ่ง) --
    draw.text((x2, y2), text_sub, font=font_sub, fill="#4A2500", stroke_width=4, stroke_fill="#2B1400") # เงา/ขอบเข้ม
    draw.text((x2, y2), text_sub, font=font_sub, fill="#FFD700") # ตัวอักษรสีทองสว่าง

    # 7. บันทึกและส่งภาพเข้า Telegram
    output_path = "output.jpg"
    img.save(output_path)

    caption = "ไม่รวยงวดนี้ จะไปรวยงวดไหน!🍀"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    
    with open(output_path, "rb") as photo:
        payload = {"chat_id": CHAT_ID, "caption": caption}
        files = {"photo": photo}
        res = requests.post(url, data=payload, files=files)

    return {"status": "success", "telegram_response": res.json()}
