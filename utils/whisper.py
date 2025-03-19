import whisper

from pydub import AudioSegment

async def transribate(voice):
    voice = message.voice
    file_id = voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path