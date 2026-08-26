import os
import random
from PIL import Image, ImageDraw, ImageFont

# 1. สุ่มตัวเลข 2 ตัว 2 ชุด และเลขวิ่ง 1 ตัว
set1 = f"{random.randint(0, 99):02d}"
set2 = f"{random.randint(0, 99):02d}"
running_num = f"{random.randint(0, 9)}"

# 2. เปิดรูปภาพ Template
img_path = "ves_template.jpg"
img = Image.open(img_path)
draw = ImageDraw.Draw(img)
img_width, img_height = img.size

# 3. โหลดฟอนต์ (เซฟความปลอดภัยถ้าไม่มีไฟล์ฟอนต์ในเครื่อง)
font_size_main = 75
font_size_sub = 50

try:
  font_main = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size_main)
  font_sub = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size_sub)
except:
  font_main = ImageFont.load_default()
  font_sub = ImageFont.load_default()

# 4. ข้อความที่จะแสดงผล
text_main = f"{set1} - {set2}"
text_sub = f"วิ่ง {running_num}"

# 5. คำนวณตำแหน่งจัดให้อยู่กึ่งกลางภาพ (Center Alignment)
bbox1 = draw.textbbox((0, 0), text_main, font=font_main)
w1 = bbox1[2] - bbox1[0]
x1 = (img_width - w1) / 2
y1 = (img_height / 2) - 80  # ปรับความสูงบรรทัดแรก

bbox2 = draw.textbbox((0, 0), text_sub, font=font_sub)
w2 = bbox2[2] - bbox2[0]
x2 = (img_width - w2) / 2
y2 = y1 + 100  # ปรับระยะห่างระหว่างบรรทัด

# 6. วาดข้อความลงบนภาพ
draw.text((x1, y1), text_main, fill="#053B18", font=font_main)  # สีเขียวเข้มเด่นๆ
draw.text((x2, y2), text_sub, fill="#C59B27", font=font_sub)  # สีทองเด่นๆ

# 7. เซฟภาพไว้ส่ง
output_path = "output.jpg"
img.save(output_path)
