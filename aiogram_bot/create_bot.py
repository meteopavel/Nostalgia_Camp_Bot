from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import os

load_dotenv()

# переменные для работы
ADMIN_ID = os.getenv('ADMIN_ID')
API_TOKEN = os.getenv('API_TOKEN')
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
WEBHOOK_PATH = f'/{API_TOKEN}'
WEBHOOK_URL = os.getenv('WEBHOOK_URL')


# инициализируем бота и диспетчера для работы с ним
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
