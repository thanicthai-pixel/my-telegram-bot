import random
from PIL import Image, ImageDraw, ImageFont

# 1. สุ่มตัวเลขใหม่ตามที่ต้องการ
set1 = f"{random.randint(0, 99):02d}"  # ชุดที่ 1 (บน-ล่าง)
set2 = f"{random.randint(0, 99):02d}"  # ชุดที่ 2 (บน-ล่าง)
running_num = f"{random.randint(0, 9)}"  # เลขวิ่ง 1 ตัว

# 2. เปิดรูป Template
img = Image.open("ves_template.jpg")
draw = ImageDraw.Draw(img)
img_width, img_height = img.size

# 3. กำหนดฟอนต์และขนาด (ปรับขนาดให้ใหญ่และเด่นขึ้น)
try:
  # ปรับขนาดตัวเลขชุดบน-ล่างให้เด่น
  font_main = ImageFont.truetype("arial.ttf", 65)
  # ฟอนต์สำหรับเลขวิ่ง
  font_sub = ImageFont.truetype("arial.ttf", 45)
except:
  font_main = ImageFont.load_default()
  font_sub = ImageFont.load_default()

# 4. ข้อความที่จะแสดง
text_top_bot = f"{set1} - {set2}"
text_run = f"วิ่ง {running_num}"

# 5. คำนวณตำแหน่งให้อยู่ "กึ่งกลาง" ภาพพอดี (Center Alignment)
# คำนวณขนาดข้อความชุดหลัก
bbox1 = draw.textbbox((0, 0), text_top_bot, font=font_main)
w1 = bbox1[2] - bbox1[0]
x1 = (img_width - w1) / 2
y1 = (
    img_height / 2 - 60
)  # ปรับความสูงขึ้นลงได้ตรงนี้ (ค่าลบคือเลื่อนขึ้น / บวกคือเลื่อนลง)

# คำนวณขนาดข้อความเลขวิ่ง
bbox2 = draw.textbbox((0, 0), text_run, font=font_sub)
w2 = bbox2[2] - bbox2[0]
x2 = (img_width - w2) / 2
y2 = y1 + 80  # ระยะห่างระหว่างบรรทัดแรกกับเลขวิ่ง

# 6. วาดข้อความลงบนภาพ (กำหนดสีให้เด่นชัด เช่น สีเขียวเข้มตัดกับทอง)
# วาดเงาหรือตัวหนังสือหลัก
draw.text((x1, y1), text_top_bot, fill="#0b4619", font=font_main)  # สีเขียวเข้ม
draw.text((x2, y2), text_run, fill="#b8860b", font=font_sub)  # สีทอง
