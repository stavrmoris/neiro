from aiogram.enums import ContentType
from aiogram.utils.keyboard import InlineKeyboardBuilder

import utils.database as db

from aiogram import Router, F, Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, LabeledPrice, FSInputFile, \
    PreCheckoutQuery
from aiogram.fsm.context import FSMContext
from config import CHANEL_ID
from utils.check_in_chanel import check_in_chanel
from states.states import States
from datetime import datetime, timedelta

title = "Подписка на бота"
description = "Активация подписки на бота на 1 месяц"
payload = "unique-payload-stars-123"
provider_token = "381764678:TEST:108369"


async def sub(call: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = call.message.chat.id

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ Оплата TG stars", callback_data='stars')],
        [InlineKeyboardButton(text="💳 Оплата картой", callback_data='card')],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data='start')],
    ])

    await call.message.answer('''Подписка ⚡️Plus:

- GPT-4o mini — безлимитно;
- GPT-4o — 100 запросов в день;
- GPT-4 Vision (Распознавание изображений);
- Flux - 30 запросов в день;

Стоимость: 350р в месяц''', reply_markup=keyboard)


async def stars(call: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = call.message.chat.id

    prices = [LabeledPrice(label=f'Оплата {160}', amount=160)]
    await bot.send_invoice(
        chat_id=user_id,
        title=title,
        description=description,
        payload=payload,
        photo_url='https://stavrgptbot.pythonanywhere.com/static/album.jpg',
        photo_width=416,
        photo_height=234,
        photo_size=416,
        is_flexible=False,
        provider_token=provider_token,
        currency='XTR',
        prices=prices,
    )


async def card(call: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = call.message.chat.id

    prices = [LabeledPrice(label=f'Оплата {350}', amount=int(350) * 100)]
    await bot.send_invoice(
        chat_id=user_id,
        title=title,
        description=description,
        payload=payload,
        photo_url='https://stavrgptbot.pythonanywhere.com/static/album.jpg',
        photo_width=416,
        photo_height=234,
        photo_size=416,
        is_flexible=False,
        provider_token=provider_token,
        currency='rub',
        prices=prices,
    )


async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


async def successful_payment(message: Message):
    user_id = message.chat.id

    await message.answer('Все очи-чпоки!')
    today = datetime.now()
    future_date = today + timedelta(days=30)
    db.set_variable(user_id, 'data', future_date.strftime('%Y-%m-%d'))
    db.set_variable(user_id, 'gpt4o-usage', 100)
    db.set_variable(user_id, 'dalle-usage', 30)
    db.set_variable(user_id, 'gpt4omini-usage', 100000)


def router(rt: Router):
    rt.callback_query.register(sub, F.data == 'sub')
    rt.callback_query.register(stars, F.data == 'stars')
    rt.callback_query.register(card, F.data == 'card')

    rt.message.register(successful_payment, F.content_type == ContentType.SUCCESSFUL_PAYMENT)
    rt.pre_checkout_query.register(pre_checkout_query, lambda query: True)
