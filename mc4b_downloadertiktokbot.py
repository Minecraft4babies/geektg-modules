"""
    ____  __  __ _                            __ _   _  _   _           _     _
   / __ \|  \/  (_)_ __   ___  ___ _ __ __ _ / _| |_| || | | |__   __ _| |__ (_) ___  ___
  / / _` | |\/| | | '_ \ / _ \/ __| '__/ _` | |_| __| || |_| '_ \ / _` | '_ \| |/ _ \/ __|
 | | (_| | |  | | | | | |  __/ (__| | | (_| |  _| |_|__   _| |_) | (_| | |_) | |  __/\__ \
  \ \__,_|_|  |_|_|_| |_|\___|\___|_|  \__,_|_|  \__|  |_| |_.__/ \__,_|_.__/|_|\___||___/
   \____/
"""
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from .. import loader, utils

def register(cb):
    cb(DownloaderTiktokBotMod())

@loader.tds
class DownloaderTiktokBotMod(loader.Module):
    """Скачиваю видео TikTok через @downloader_tiktok_bot"""
    strings = {"cfg_doc": "Настройка надписей состояния работы",
               "name": "DownloaderTiktokBot",
               "NoArgs": "<b>🐈‍⬛: «Миу? Что ты хочешь сделать? Я жду ссылку..»</b>",
               "Working": "<b>Котики(🐈‍⬛ и 🐈) сохраняют твою штучку...🐾</b>",
               "Working_checker": "<b>Ой, котик увидел от тебя ссылку!!!🐾</b>",
               "BlockedBotError": "<b>🐈: «Няф, разблокируй, пожалуйста, @allsaverbot!»</b>",
               "TimeoutError": "<b>🐈‍⬛: «Бот @downloader_tiktok_bot что-то вредничает...🐾»</b>"}

    def __init__(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self.me = await client.get_me()

    def __init__(self):
        self.config = loader.ModuleConfig(
            "CheckedChats", "Нужен ID чата(ов)", lambda: "Чаты, в которых работает авто-скачивание(через пробел)")



    @loader.unrestricted
    async def мурcmd(self, message):
        """ссылка / <реплай>


        👨‍💻Made by: @Minecraft4babies_GFTG_Modules"""

        try:
            text = utils.get_args_raw(message)
            reply = await message.get_reply_message()
            bot_chat = "@downloader_tiktok_bot"
            if not text and not reply:
                if message.out:
                    await message.edit(self.strings('NoArgs'))
                else:
                    await message.client.send_message(message.chat_id, message=self.strings('NoArgs'), reply_to=message)
                return
            if text:
                if message.out:
                    await message.edit(self.strings('Working'))
                else:
                    answer = await message.client.send_message(message.chat_id, message=self.strings('Working'), reply_to=message)
                async with message.client.conversation(bot_chat) as conv:
                    try:
                        await message.client.send_message(bot_chat, text)
                        response = await conv.wait_event(events.NewMessage(incoming=True, from_users=1332941342))
                    except YouBlockedUserError:
                        await message.reply(self.strings('BlockedBotError'))
                        return
                    if message.out:
                        await message.delete()
                    else:
                        await answer.delete()
                    await message.client.send_file(message.chat_id, response.media, reply_to=reply)
            else:
                if message.out:
                    await message.edit(self.strings('Working'))
                else:
                    answer = await message.client.send_message(message.chat_id, message=self.strings('Working'), reply_to=message)
                async with message.client.conversation(bot_chat) as conv:
                    try:
                        await message.client.send_message(bot_chat, reply)
                        response = await conv.wait_event(events.NewMessage(incoming=True, from_users=1332941342))
                    except YouBlockedUserError:
                        if message.out:
                            await message.reply(self.strings('BlockedBotError'))
                        else:
                            await answer.edit(self.strings('BlockedBotError'))
                        return
                    await message.client.send_file(message.chat_id, response.media, reply_to=reply)
                    if message.out:
                        await message.delete()
                    else:
                        await answer.delete()
        except:
            if message.out:
                return await message.edit(self.strings('TimeoutError'))
            else:
                return await answer.edit(self.strings('TimeoutError'))

    async def watcher(self, message):
        chat = str(message.chat_id)
        text = message.raw_text
        if chat in str(self.config['CheckedChats']) and not ' ' in text:
            if 'tiktok.com/' in text:
                try:
                    answer = await message.client.send_message(message.chat_id, message=self.strings('Working_checker'), reply_to=message)
                    bot_chat = "@downloader_tiktok_bot"
                    async with message.client.conversation(bot_chat) as conv:
                        try:
                            await message.client.send_message(bot_chat, message=text.split('=')[0])
                            response = await conv.wait_event(events.NewMessage(incoming=True, from_users=1332941342))
                        except YouBlockedUserError:
                            await answer.edit(self.strings('BlockedBotError'))
                            return
                    await message.client.send_file(message.chat_id, response.media, reply_to=message)
                    await answer.delete()
                except:
                    return await answer.edit(self.strings('TimeoutError'))
