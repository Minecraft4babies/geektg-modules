"""
    ____  __  __ _                            __ _   _  _   _           _     _           
   / __ \|  \/  (_)_ __   ___  ___ _ __ __ _ / _| |_| || | | |__   __ _| |__ (_) ___  ___ 
  / / _` | |\/| | | '_ \ / _ \/ __| '__/ _` | |_| __| || |_| '_ \ / _` | '_ \| |/ _ \/ __|
 | | (_| | |  | | | | | |  __/ (__| | | (_| |  _| |_|__   _| |_) | (_| | |_) | |  __/\__ \
  \ \__,_|_|  |_|_|_| |_|\___|\___|_|  \__,_|_|  \__|  |_| |_.__/ \__,_|_.__/|_|\___||___/
   \____/                                                                                 
"""
from .. import loader, utils
import logging
from telethon import events
from telethon import functions
import os
import ffmpeg
from .. import loader, utils


def register(cb):
    cb(mc4b_togifstickerMod())


@loader.tds
class Mc4bToGifStickerMod(loader.Module):
    """"Модуль для преобразования видео в GIF-стикеры"""
    strings = {"cfg_doc": "Настройка надписей состояния работы",
               "name": "GifSticker",
               "Downloading": "<b>Котики(🐈‍⬛ и 🐈) скачивают твою штучку...🐾</b>",
               "Converting": "<b>Котик 🐈 шаманит над твоей штучкой...🐾</b>",
               "Sending": "<b>Котик 🐈‍⬛ отправляет твою штучку...🐾</b>",
               "WrongFormatError": "<b>🐈: «Няф, это не нужный нам файлик»</b>",
               "UnexpectedError": "<b>🐈‍⬛: «Миу?!! Что-то не вышло...»</b>",
               "NoFileError": "<b>🐈: «Миу?!! Я не вижу никакого файла...»</b>"}

    def __init__(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self.me = await client.get_me()

    @loader.unrestricted
    async def gifstickercmd(self, message):
        """ <реплай на видео>
        
        
        👨‍💻Made by: @Minecraft4babies_GFTG_Modules"""

        a = """ffmpeg -ss 00:00:00 -i inputfile.mp4 -to 00:00:03 -filter:v "scale=w=512:h=512:force_original_aspect_ratio=decrease" -r 24 -c:v libvpx-vp9 -crf 30 -b:v 600k -an GifSticker.WEBM"""
        try:
            await message.edit(self.strings("Downloading", message))
            reply = await message.get_reply_message()
            if reply:
                if reply.video:
                    await message.client.download_media(reply.media, "inputfile.mp4")
                    await message.edit(self.strings("Converting", message))
                    os.system(a)
                    await message.edit(self.strings("Sending", message))
                    await message.client.send_file(message.to_id, "GifSticker.WEBM", force_document=True, reply_to=reply)
                else:
                    return await message.edit(self.strings("WrongFormatError", message))
                await message.delete()
                os.remove('GifSticker.WEBM')
                os.remove('inputfile.mp4')
            else:
                return await message.edit(self.strings("NoFileError"))
        except:
            await message.edit(self.strings("UnexpectedError", message))
            os.remove('GifSticker.WEBM')
            os.remove('inputfile.mp4')
            return
