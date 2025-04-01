import utils.database as db

from aiogram import Router, F, Dispatcher, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from config import CHANEL_ID
from utils.check_in_chanel import check_in_chanel
from states.states import States


async def msg_start(message: Message, state: FSMContext, bot: Bot):
    user_id = message.chat.id

    db.add_user_to_list(user_id)

    if db.get_variable(user_id, 'neiro') is None or db.get_variable(user_id, 'neiro') == '':
        db.set_variable(user_id, 'neiro', 'gpt-4o-mini')

    if await check_in_chanel(bot, user_id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подписаться", url=f"https://t.me/{CHANEL_ID}")],
            [InlineKeyboardButton(text="🚀 Продолжить", callback_data='start')]
        ])
        await message.answer('''🤖 Это *абсолютно бесплатный бот* для работы с базовыми нейросетями. 

❗Перед использованием бота, пожалуйста, подпишитесь на [наш канал](https://t.me/epichero_dev).''', reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💰 Подписка", callback_data='sub'),
             InlineKeyboardButton(text="🤖 Нейросети", callback_data='neiro')],
            [InlineKeyboardButton(text="🆘 Тех. поддержка", url=f"https://t.me/stavrmoris")],
        ])
        neiro = db.get_variable(user_id, 'neiro')
        neiro_txt = '*GPT-4o*'
        if neiro == 'gpt-4o-mini':
            neiro_txt = '*GPT-4o mini*'
        elif neiro == 'dall-e-3':
            neiro_txt = '*Flux*'

        gpt4o_usage = db.get_variable(user_id, 'gpt4o-usage')
        dalle_usage = db.get_variable(user_id, 'dalle-usage')
        gpt4omini_usage = db.get_variable(user_id, 'gpt4omini-usage')
        if gpt4o_usage is None:
            gpt4o_usage = 'Отсутствует подписка'
        if dalle_usage is None:
            dalle_usage = 'Отсутствует подписка'
        if gpt4omini_usage is None:
            gpt4omini_usage = db.set_variable(user_id, 'gpt4omini-usage', 30)
        else:
            if int(gpt4omini_usage) > 30:
                gpt4omini_usage = '♾️'

        await message.answer(f'''
🤖 Это *абсолютно бесплатный бот* для работы с базовыми нейросетями. Кол-во генерация можно увеличить вдвое, если оформить подписку и, тем самым, поддержать автора. Если возникли проблемы - пишите @stavrmoris с подробным баг репортом.

✴️ Баланс генераций:
⭐ *GPT-4o mini*: {gpt4omini_usage};
⭐ *GPT-4o*: {gpt4o_usage};
⭐ *Flux*: {dalle_usage}.

✳️ Текущая нейросеть: {neiro_txt}

👇 Для старта работы просто напишите вопрос в чат!''', reply_markup=keyboard)
        await state.set_state(States.waiting_for_prompt)


async def call_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = call.message.chat.id

    db.add_user_to_list(user_id)

    await call.message.delete()
    if await check_in_chanel(bot, user_id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подписаться", url=f"https://t.me/{CHANEL_ID}")],
            [InlineKeyboardButton(text="🚀 Продолжить", callback_data='start')]
        ])
        await call.message.answer('''🤖 Это *абсолютно бесплатный бот* для работы с базовыми нейросетями. 

❗Перед использованием бота, пожалуйста, подпишитесь на [наш канал](https://t.me/epichero_dev).''', reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💰 Подписка", callback_data='sub'),
             InlineKeyboardButton(text="🤖 Нейросети", callback_data='neiro')],
            [InlineKeyboardButton(text="🆘 Тех. поддержка", url=f"https://t.me/stavrmoris")],
        ])
        neiro = db.get_variable(user_id, 'neiro')
        neiro_txt = '*GPT-4o*'
        if neiro == 'gpt-4o-mini':
            neiro_txt = '*GPT-4o mini*'
        elif neiro == 'dall-e-3':
            neiro_txt = '*Flux*'

        gpt4o_usage = db.get_variable(user_id, 'gpt4o-usage')
        dalle_usage = db.get_variable(user_id, 'dalle-usage')
        gpt4omini_usage = db.get_variable(user_id, 'gpt4omini-usage')
        if gpt4o_usage is None:
            gpt4o_usage = 'Отсутствует подписка'
        if dalle_usage is None:
            dalle_usage = 'Отсутствует подписка'
        if gpt4omini_usage is None:
            gpt4omini_usage = db.set_variable(user_id, 'gpt4omini-usage', 30)
        else:
            if int(gpt4omini_usage) > 30:
                gpt4omini_usage = '♾️'

        await call.message.answer(f'''
🤖 Это *абсолютно бесплатный бот* для работы с базовыми нейросетями. Кол-во генерация можно увеличить вдвое, если оформить подписку и, тем самым, поддержать автора. Если возникли проблемы - пишите @stavrmoris с подробным баг репортом.

✴️ Баланс генераций:
⭐ *GPT-4o mini*: {gpt4omini_usage};
⭐ *GPT-4o*: {gpt4o_usage};
⭐ *Flux*: {dalle_usage}.

✳️ Текущая нейросеть: {neiro_txt}

👇 Для старта работы просто напишите вопрос в чат!''', reply_markup=keyboard)
        await state.set_state(States.waiting_for_prompt)


def router(rt: Router):
    rt.message.register(msg_start, CommandStart())
    rt.callback_query.register(call_start, F.data == 'start')
