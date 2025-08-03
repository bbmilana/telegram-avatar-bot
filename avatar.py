import asyncio
import os
from telethon import TelegramClient, functions
from telethon.tl.functions.photos import DeletePhotosRequest
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta

# Читаем переменные окружения
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
session_name = 'session_d_avatar'

# Настройки картинки
img_size = (400, 400)
bg_color = (240, 240, 240)
text_color = (0, 0, 0)
font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'  # шрифт, доступный в Linux на Render
font_size = 100

async def update_avatar(client):
    photos = await client.get_profile_photos('me')
    if photos:
        await client(DeletePhotosRequest(photos))

    target_time = datetime.now() + timedelta(seconds=3)
    now_text = target_time.strftime('%H:%M')

    img = Image.new('RGB', img_size, bg_color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)

    bbox = draw.textbbox((0, 0), now_text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pos = ((img_size[0] - w) // 2, (img_size[1] - h) // 2)
    draw.text(pos, now_text, font=font, fill=text_color)

    img.save('avatar.png')
    file = await client.upload_file('avatar.png')

    await client(functions.photos.UploadProfilePhotoRequest(file=file))
    print(f'✅ Аватар обновлён: {now_text}')

async def main():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start(bot_token=bot_token)

    while True:
        try:
            await update_avatar(client)
        except Exception as e:
            print(f'❌ Ошибка обновления: {e}')
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
