from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Бот-путеводитель поможет тебе в поиске нужной информации про определенный город России.')

@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
     await message.answer(
        'Напиши название города, который тебе интересен,'
        'а я расскажу про его интересные достопримечательности'
    )
    