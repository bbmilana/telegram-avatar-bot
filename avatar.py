import asyncio
from telethon import TelegramClient, functions
from telethon.tl.functions.photos import DeletePhotosRequest
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta

# Вставьте свои ключи из my.telegram.org
api_id       = 26401759
api_hash     = 'c1a8c2c73c495004e9c1ccc5845b743f'
session_name = 'session_dyn_avatar'

# Настройки картинки
img_size   = (400, 400)
bg_color   = (240, 240, 240)     # фон ты можешь изменить здесь
text_color = (0, 0, 0)

# Попробуем более "модный" шрифт — Consolas
font_path  = 'C:\\Windows\\Fonts\\consola.ttf'  # убедись, что он есть (или замени)
font_size  = 100

async def update_avatar(client):
    # Удаляем старые аватары
    photos = await client.get_profile_photos('me')
    if photos:
        await client(DeletePhotosRequest(photos))

    # Время через 3 секунды (немного заранее)
    target_time = datetime.now() + timedelta(seconds=3)
    now_text = target_time.strftime('%H:%M')

    # Создаём изображение
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
    await client.start()

    while True:
        try:
            await update_avatar(client)
        except Exception as e:
            print(f'❌ Ошибка обновления: {e}')
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
