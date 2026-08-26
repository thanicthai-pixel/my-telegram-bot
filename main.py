import random
import os
import requests
from fastapi import FastAPI
from PIL import Image, ImageDraw, ImageFont
from telegram import Bot

app = FastAPI()

TELEGRAM_TOKEN = "8825722253:AAFIyG1d6US4XOkbsoI55SzkREYRZblNgEI"
CHAT_ID = "1880260879"

FONT_PATH = "Sarabun-Bold.ttf"
if not os.path.exists(FONT_PATH):
    font_url = "https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Bold.ttf"
    res = requests.get(font_url)
    with open(FONT_PATH, "wb") as f:
        f.write(res.content)

def create_lucky_image():
    num_top = f"{random.randint(0, 9999):04d}"
    num_bottom = f"{random.randint(0, 99):02d}"

    if os.path.exists("ves_template.jpg"):
        img = Image.open("ves_template.jpg").convert("RGB")
    else:
        img = Image.new("RGB", (1024, 1024), color=(15, 20, 25))

    draw = ImageDraw.Draw(img)
    font_number_big = ImageFont.truetype(FONT_PATH, 90)
    font_number_sub = ImageFont.truetype(FONT_PATH, 60)
    
    dark_green = (20, 60, 40)
    gold_color = (212, 160, 23)

    draw.text((360, 400), f"{num_top}", font=font_number_big, fill=dark_green)
    draw.text((440, 530), f"เลขท้าย: {num_bottom}", font=font_number_sub, fill=gold_color)

    image_path = "final_ves_lucky.jpg"
    img.save(image_path)
    return image_path

@app.get("/")
def home():
    return {"status": "Bot Server Online"}

@app.get("/send-lottery")
async def send_lottery():
    image_path = create_lucky_image()
    bot = Bot(token=TELEGRAM_TOKEN)
    
    with open(image_path, "rb") as photo:
        await bot.send_photo(
            chat_id=CHAT_ID, 
            photo=photo, 
            caption="งวดนี้รวย! ไม่รวยงวดนี้ จะไปรวยงวดไหน!🍀"
        )
    return {"message": "Success"}
