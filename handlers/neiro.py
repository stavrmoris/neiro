import utils.database as db

from aiogram import Router, F, Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from config import CHANEL_ID
from utils.check_in_chanel import check_in_chanel
from states.states import States


async def neiro_choice(call: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = call.message.chat.id

    if call.data.startswith('neiro_'):
        db.set_variable(user_id, 'neiro', call.data.split('_')[1])

    neiro = db.get_variable(user_id, 'neiro')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{'✅' if neiro == 'gpt-4o' else ''} GPT-4o", callback_data='neiro_gpt-4o'),
         InlineKeyboardButton(text=f"{'✅' if neiro == 'gpt-4o-mini' else ''} GPT-4o mini", callback_data='neiro_gpt-4o-mini')],
        [InlineKeyboardButton(text=f"{'✅' if neiro == 'dall-e-3' else ''} Flux", callback_data='neiro_dall-e-3')],
        [InlineKeyboardButton(text=f"⬅️ Назад", callback_data='start')]
    ])

    await call.message.delete()
    await call.message.answer('''🤖 Выберите нейросеть:

1. ChatGPT-4o
Основная модель с высоким интеллектом. Оптимальна для большинства задач. 

2. ChatGPT-4o mini
Доступная небольшая модель для быстрых и простых задач.

3. Flux
Модель для генерации реалистичных изображений''', reply_markup=keyboard)


def router(rt: Router):
    rt.callback_query.register(neiro_choice, F.data == 'neiro')
    rt.callback_query.register(neiro_choice, F.data.startswith('neiro_'))
