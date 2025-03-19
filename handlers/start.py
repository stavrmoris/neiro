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
        await message.answer('''❤️ Я — твой главный помощник в жизни, который ответит на любой вопрос, поддержит тебя, сделает за тебя задание, выполнит любую работу или нарисует картину.

Перед использованием бота, пожалуйста, подпишитесь на [наш канал](https://t.me/epichero_dev).

✳️ Мы просим так сделать для защиты от ботов и за это мы дарим вам 30 бесплатных запросов в ChatGPT, которые обновляются каждые 24 часа.''', reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💰 Подписка", callback_data='sub'),
             InlineKeyboardButton(text="🤖 Нейросети", callback_data='neiro')],
            [InlineKeyboardButton(text="🆘 Тех. поддержка", url=f"https://t.me/stavrmoris")],
        ])
        neiro = db.get_variable(user_id, 'neiro')
        neiro_txt = '*GPT-4o mini*'
        if neiro == 'gpt-4o-mini':
            neiro_txt = '*GPT-4o*'
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

        await message.answer(f'''❤️ Я — твой верный помощник, готовый поддержать в любом деле. Задай мне вопрос, поручи задачу, доверь работу или заказ — я всегда рядом, чтобы помочь, вдохновить и сделать твой день легче. Хочешь совет, решение или даже картину? Я справлюсь!

✴️ Баланс генераций:
⭐ *GPT-4o mini*: {gpt4omini_usage};
⭐ *GPT-4o*: {gpt4o_usage};
⭐ *Flux*: {dalle_usage}.

 ⤷ Отправь мне голосовое сообщение — я тебе отвечу на твой вопрос
 ⤷ Напишу за тебя пост для блога, соцсетей, сформирую заявление или напишу полноценное сочинение 
 ⤷ Решу любое задание или выполню работу за тебя
 ⤷ Нарисую для тебя картину с помощью Flux
 ⤷ Побуду твоим личным психологом или лучшим другом 

✳️ Текущая нейросеть: {neiro_txt}

❗️ Чтобы сгенерировать изображение, пожалуйста, выберите Flux

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
        await call.message.answer('''❤️ Я — твой главный помощник в жизни, который ответит на любой вопрос, поддержит тебя, сделает за тебя задание, выполнит любую работу или нарисует картину.

Перед использованием бота, пожалуйста, подпишитесь на [наш канал](https://t.me/epichero_dev).

✳️ Мы просим так сделать для защиты от ботов и за это мы дарим вам 30 бесплатных запросов в ChatGPT, которые обновляются каждые 24 часа.''', reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💰 Подписка", callback_data='sub'),
             InlineKeyboardButton(text="🤖 Нейросети", callback_data='neiro')],
            [InlineKeyboardButton(text="🆘 Тех. поддержка", url=f"https://t.me/stavrmoris")],
        ])
        neiro = db.get_variable(user_id, 'neiro')
        neiro_txt = '*GPT-4o mini*'
        if neiro == 'gpt-4o-mini':
            neiro_txt = '*GPT-4o*'
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

        await call.message.answer(f'''❤️ Я — твой верный помощник, готовый поддержать в любом деле. Задай мне вопрос, поручи задачу, доверь работу или заказ — я всегда рядом, чтобы помочь, вдохновить и сделать твой день легче. Хочешь совет, решение или даже картину? Я справлюсь!

✴️ Баланс генераций:
⭐ *GPT-4o mini*: {gpt4omini_usage};
⭐ *GPT-4o*: {gpt4o_usage};
⭐ *Flux*: {dalle_usage}.

 ⤷ Отправь мне голосовое сообщение — я тебе отвечу на твой вопрос
 ⤷ Напишу за тебя пост для блога, соцсетей, сформирую заявление или напишу полноценное сочинение 
 ⤷ Решу любое задание или выполню работу за тебя
 ⤷ Нарисую для тебя картину с помощью Flux
 ⤷ Побуду твоим личным психологом или лучшим другом 

✳️ Текущая нейросеть: {neiro_txt}

❗️ Чтобы сгенерировать изображение, пожалуйста, выберите Flux

👇 Для старта работы просто напишите вопрос в чат!''', reply_markup=keyboard)
        await state.set_state(States.waiting_for_prompt)


def router(rt: Router):
    rt.message.register(msg_start, CommandStart())
    rt.callback_query.register(call_start, F.data == 'start')
