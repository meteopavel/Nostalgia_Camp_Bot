from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton,
    InputMediaPhoto
)
from services.upload_static import load_file_ids

from services.create_bot import ADMIN_ID

router = Router()


def get_category_keyboard():
    buttons = [
        KeyboardButton(text='🏠 Домики'),
        KeyboardButton(text='🎉 Развлечения'),
        KeyboardButton(text='🌳 Территория'),
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button] for button in buttons],
        resize_keyboard=True
    )
    return keyboard


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        'Приветвуем, уважаемые гости! 👋\n\n'
        'Чтобы узнать, как работать с ботом, нажмите /help\n'
        'Или можете посмотреть команды в меню',
    )


@router.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    await message.answer(
        '📸 <b>Инструкции по работе с ботом</b> 🤖:\n\n'
        '✨ Нажмите на кнопки ниже, чтобы увидеть фотографии турбазы 🏞️🏡🌳.\n'
        '✍️ Вы можете написать любое сообщение, и оно будет отправлено '
        'администратору 💬.\n\n'
        '💡 <i>Если остались вопросы, свяжитесь с администратором через '
        'сообщение 👤.</i>',
        reply_markup=get_category_keyboard()
    )


async def send_photos_by_category(message: Message, category: str):
    file_ids = load_file_ids()
    media = [
        InputMediaPhoto(media=data['file_id'], caption=f'{filename}')
        for filename, data in file_ids.items()
        if data.get('category') == category
    ]
    await message.answer_media_group(media=media)


@router.message(lambda message: message.text == '🏠 Домики')
async def show_houses_handler(message: Message):
    await send_photos_by_category(message, 'houses')


@router.message(lambda message: message.text == '🎉 Развлечения')
async def show_entertainment_handler(message: Message):
    await send_photos_by_category(message, 'entertainment')


@router.message(lambda message: message.text == '🌳 Территория')
async def show_territory_handler(message: Message):
    await send_photos_by_category(message, 'territory')


@router.message()
async def forward_to_admin(message: Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    text = message.text

    admin_message = (
        f'📩 Новое сообщение от пользователя:\n'
        f'👤 Имя: {user_name}\n'
        f'🆔 ID: {user_id}\n'
        f'💬 Текст: {text}'
    )

    await message.bot.send_message(ADMIN_ID, admin_message)

    await message.answer('✅ Ваше сообщение отправлено администратору!')
