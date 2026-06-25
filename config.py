import os

# Получаем токен из переменных окружения Render
token = os.getenv('BOT_TOKEN')
NICNAME_BOT = os.getenv('NICNAME_BOT', 'anonimmassagingbot')
MAIN_ADMIN_ID = int(os.getenv('MAIN_ADMIN_ID', 0))

if not token:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")
