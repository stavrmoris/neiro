from config import CHANEL_ID


async def check_in_chanel(bot, user_id):
    user_channel_status = await bot.get_chat_member(chat_id=f'@{CHANEL_ID}', user_id=user_id)
    return user_channel_status.status in ["left", "kicked"]
