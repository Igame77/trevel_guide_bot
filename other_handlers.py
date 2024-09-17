from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from data_miner import miner
router = Router()

class ComputingCallBacks(CallbackData, prefix = 'any'):
    theme_id: int
    city_name: str

@router.message()
async def process_request(message : Message):
    global msg_ans
    global theme_list
    city = miner.translator_translate(message.text)
    data = miner.get_first_data(f'https://www.tourister.ru/world/europe/russia/city/{city}')
    
    if data == [] or data is None:
        await message.reply(text = 'К сожалению, я не могу ничего рассказать про этот город:(')
    else:
        theme_list = []
        buttons = []

        for h3 in data[0][:10]:
            words = h3.get_text().replace('-',' ').split()
            if len(words) > 1:
                theme_list.append(' '.join([theme[1:-2] for theme in words]))
            else:
                theme_list.append(words[0][1:-2])
            buttons.append([InlineKeyboardButton(text = h3.get_text(), callback_data=ComputingCallBacks(theme_id = data[0].index(h3), city_name = city).pack())])

        keyboard = InlineKeyboardMarkup(inline_keyboard= buttons)
        await message.answer(data[1])
        await message.answer('\n-------------\n'.join([el.get_text() for el in data[0][:10]]),reply_markup=keyboard)
        msg_ans = await message.answer(text = 'Выберите нужную Вам тему...')

    
@router.callback_query(ComputingCallBacks.filter())
async def process_callback_btns(callback : CallbackQuery, callback_data : ComputingCallBacks):
    global msg_ans
    global theme_list
    url = f'https://www.tourister.ru/world/europe/russia/city/{callback_data.city_name}'
    data = miner.get_subtext(url, theme_list[callback_data.theme_id])
    await msg_ans.delete()
    if data != []:
        msg_ans = await callback.message.answer(text = '\n'.join(data[:5]))
    else: msg_ans = await callback.message.answer(text = f'Подробнее на {url}')
