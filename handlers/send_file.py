# (c) @JAsuran

import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from handlers.helpers import str_to_b64


async def reply_forward(message: Message, file_id: int):
    try:
        await message.reply_text(
            f"**Files will be Deleted After 2 min**\n\n"
            f"**__To Retrive the Stored File, just again open the link!__**\n\n"
            f"**Link:** https://telegram.me/{Config.BOT_USERNAME}?start=JAsuran_{str_to_b64(str(file_id))}",
            disable_web_page_preview=True, quote=True)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await reply_forward(message, file_id)


async def media_forward(bot: Client, user_id: int, file_id: int):
    try:
        if Config.FORWARD_AS_COPY is True:
            return await bot.copy_message(chat_id=user_id, from_chat_id=Config.DB_CHANNEL,
                                          message_id=file_id)
        elif Config.FORWARD_AS_COPY is False:
            return await bot.forward_messages(chat_id=user_id, from_chat_id=Config.DB_CHANNEL,
                                              message_ids=file_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return media_forward(bot, user_id, file_id)
    
async def delete_file(file_id: int):

    await asyncio.sleep(120)  # wait for 2 minutes

    # Delete the file using the file ID

    # Code to delete the file goes here


async def send_media_and_reply(bot: Client, user_id: int, file_id: int):
    sent_message = await media_forward(bot, user_id, file_id)
    await reply_forward(message=sent_message, file_id=file_id)
        #await asyncio.sleep(2)

# Delete the message after 2 minutes
    await asyncio.sleep(120)
    try:
        await sent_message.delete()
    except Exception as e:
        print(f"Error deleting message {sent_message.message_id}: {e}")
