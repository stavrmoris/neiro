from datetime import datetime

import utils.database as db
import whisper
import os

from pydub import AudioSegment
from aiogram import Router, F, Dispatcher, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from config import CHANEL_ID
from utils.dalle import image_generate
from utils.gpt4o import text_generate
from states.states import States

# model = whisper.load_model("base")


async def neiro_create(message: Message, state: FSMContext, bot: Bot):
    user_id = message.chat.id

    prompt = message.text

    # if message.voice:
    #     # Скачиваем голосовое сообщение
    #     voice = message.voice
    #     file_id = voice.file_id
    #     file = await bot.get_file(file_id)
    #     file_path = file.file_path
    #
    #     # Сохраняем файл локально
    #     downloaded_file = await bot.download_file(file_path)
    #     ogg_file_path = f"tmp_voice/voice_message_{user_id}.ogg"
    #     with open(ogg_file_path, "wb") as f:
    #         f.write(downloaded_file.read())
    #
    #     # Преобразуем .ogg в .wav с помощью pydub
    #     audio = AudioSegment.from_file(ogg_file_path, format="ogg")
    #     wav_file_path = f"tmp_voice/converted_{user_id}.wav"
    #     audio.export(wav_file_path, format="wav")
    #
    #     # Расшифровываем аудио с помощью Whisper
    #     result = model.transcribe(wav_file_path)
    #     prompt = result["text"]
    #     print(prompt)
    #     os.remove(ogg_file_path)
    #     os.remove(wav_file_path)

    # Получаем данные о нейросети и лимитах
    neiro = db.get_variable(user_id, 'neiro')
    usage_data = {
        'gpt-4o': db.get_variable(user_id, 'gpt4o-usage'),
        'gpt-4o-mini': db.get_variable(user_id, 'gpt4omini-usage'),
        'dall-e-3': db.get_variable(user_id, 'dalle-usage'),
    }

    # Функции для генерации текста и изображений
    generate_functions = {
        'gpt-4o': text_generate,
        'gpt-4o-mini': text_generate,
        'dall-e-3': image_generate,
    }

    # Сообщение о загрузке
    msg = await message.answer('⌛ Подождите, идет генерация...')

    # Проверяем, есть ли лимиты для выбранной нейросети
    if neiro in usage_data and usage_data[neiro] is not None:
        if int(usage_data[neiro]) > 0:
            # Генерация ответа
            if neiro in ['gpt-4o', 'gpt-4o-mini']:
                answer = await text_generate(user_id, prompt, neiro)
                text_splits = split_text_naturally(answer)
                for split in text_splits:
                    await message.answer(split)
            elif neiro == 'dall-e-3':
                answer = await generate_functions[neiro](user_id, prompt)
                await message.answer_photo(answer)
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🤖 Выбрать нейросеть", callback_data='neiro')],
                [InlineKeyboardButton(text="⬅️ Назад", callback_data='start')],
            ])

            now = datetime.now()
            date_str = db.get_variable(user_id, 'data')
            date_to_compare = datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_str is not None and now.date() <= date_to_compare:
                await message.answer('😢 Похоже ваши генерации на сегодня закончились. Чтобы продолжить выберите другую нейросеть', reply_markup=keyboard)
            else:
                await message.answer('😢 Похоже ваши генерации закончились. Чтобы увеличить их число - приобретите подписку', reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💰 Купить подписку", callback_data='sub')],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data='start')],
        ])
        await message.answer('😢 Похоже у вас нет активной подписки. Вы можете приобрести её, нажав на кнопку под сообщением', reply_markup=keyboard)
    await msg.delete()


async def clear_context(message: Message):
    user_id = message.chat.id
    db.clear_message_history(user_id)
    await message.answer('🎉 Контекст успешно очищен!')


async def photo(message: Message):
    await message.answer('📸 Извиняемся, пока не готово :(')


def split_text_naturally(text, max_length=4000):
    """
    Разделяет текст на части по max_length символов, учитывая естественные границы (концы предложений).

    :param text: Исходный текст для разделения.
    :param max_length: Максимальная длина одной части (по умолчанию 4000 символов).
    :return: Список частей текста.
    """
    parts = []
    while len(text) > max_length:
        # Ищем последнее предложение в пределах max_length символов
        chunk = text[:max_length]
        last_sentence_end = max(
            chunk.rfind("."),
            chunk.rfind("!"),
            chunk.rfind("?")
        )

        # Если нет знаков препинания, просто разрезаем по max_length
        if last_sentence_end == -1:
            last_sentence_end = max_length

        # Добавляем часть до последнего знака препинания
        part = text[:last_sentence_end + 1].strip()
        parts.append(part)

        # Обрезаем обработанную часть из исходного текста
        text = text[last_sentence_end + 1:].strip()

    # Добавляем оставшуюся часть текста
    if text:
        parts.append(text.strip())

    return parts


def router(rt: Router):
    rt.message.register(clear_context, Command("reset"))
    rt.message.register(neiro_create, States.waiting_for_prompt, F.text)
    rt.message.register(neiro_create, States.waiting_for_prompt, F.voice)
    rt.message.register(photo, States.waiting_for_prompt, F.photo)
