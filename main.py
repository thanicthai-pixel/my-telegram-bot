import os
import random
import requests
from fastapi import FastAPI
from PIL import Image, ImageDraw, ImageFont

app = FastAPI()

# ⚠️ อย่าลืมใส่ BOT_TOKEN ของคุณที่นี่
BOT_TOKEN = os.getenv("8825722253:AAFIyG1d6US4XOkbsoI55SzkREYRZblNgEI")
CHAT_ID = os.getenv("1880260879")

# ฟังก์ชันโหลดฟอนต์ไทยสวยๆ (ดึงจาก Google Fonts อัตโนมัติถ้าไม่มีไฟล์)
def get_thai_font(size, bold=True):
    # พยายามใช้ฟอนต์ที่มีในระบบก่อน
    font_names = [
        "/usr/share/fonts/truetype/thai/Garuda.ttf", # สำหรับระบบ Linux
        "Garuda-Bold.ttf" if bold else "Garuda.ttf",
        "Prompt-Bold.ttf" if bold else "Prompt.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf" # สำหรับ macOS
    ]
    
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except:
            pass

    # ถ้าหาฟอนต์อื่นไม่ได้ ให้ใช้ Prompt จาก Google Fonts
    font_filename = "Prompt-Bold.ttf" if bold else "Prompt-Regular.ttf"
    if not os.path.exists(font_filename):
        font_base_url = "https://github.com/google/fonts/raw/main/ofl/prompt/"
        font_url = font_base_url + font_filename
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

    # 3. โหลดฟอนต์ขนาดใหญ่
    font_main = get_thai_font(80) # ขนาดเลขบน-ล่าง
    font_sub = get_thai_font(60)  # ขนาดเลขวิ่ง

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
    y2 = y1 + 100

    # 6. เทคนิคการวาดขอบและเงา (Stroke and Drop Shadow)
    # ฟังก์ชันวาดขอบเงา
    def draw_text_with_effect(x, y, text, font, fill_color="#FFD700", stroke_color="#2B1400", stroke_width=4, shadow_color="#000000", shadow_offset=(3, 3)):
        # 6.1 วาดเงา (Drop Shadow) ใต้ตัวอักษร
        shadow_x = x + shadow_offset[0]
        shadow_y = y + shadow_offset[1]
        draw.text((shadow_x, shadow_y), text, font=font, fill=shadow_color)
        
        # 6.2 วาดตัวอักษรพร้อมขอบ (Stroke) ทับด้านบน
        draw.text((x, y), text, font=font, fill=fill_color, stroke_width=stroke_width, stroke_fill=stroke_color)

    # วาดบรรทัดที่ 1 (เลข 2 ชุด)
    draw_text_with_effect(x1, y1, text_main, font_main)

    # วาดบรรทัดที่ 2 (เลขวิ่ง)
    draw_text_with_effect(x2, y2, text_sub, font_sub)

    # 7. บันทึกและส่งภาพเข้า Telegram
    output_path = "output.jpg"
    img.save(output_path)

    caption = "งวดนี้รวย! ไม่รวยงวดนี้ จะไปรวยงวดไหน!🍀"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    
    with open(output_path, "rb") as photo:
        payload = {"chat_id": CHAT_ID, "caption": caption}
        files = {"photo": photo}
        res = requests.post(url, data=payload, files=files)

    return {"status": "success", "telegram_response": res.json()}
