from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from Configs import Config
import math
import os
from io import BytesIO
from PIL import Image
from loggers import logging

bot = TelegramClient("bot", api_id=Config.API_ID, api_hash=Config.API_HASH)
stickertoimgbot = bot.start(bot_token=Config.BOT_TOKEN)
sedpath = "./starkgangz/"
if not os.path.isdir(sedpath):
    os.makedirs(sedpath)

@stickertoimgbot.on(events.NewMessage)
async def handle_message(hmm: events.NewMessage.Event):
    is_as = is_it_animated_sticker(hmm)
    okz = hmm.id
    if hmm.is_group:
        print("Sed")
        return
    if hmm.media:
        if not is_as:
            file_s = await stickertoimgbot.download_media(hmm.media, sedpath)
            resize_image(file_s, sedpath)
            file_name = "StickerToImg.png"
            okd = sedpath + "/" + file_name
        else:
            file_s = await stickertoimgbot.download_media(hmm.media, sedpath)
            file_name = "AnimatedSticker.tgs"
            okd = sedpath + "/" + file_name
        await stickertoimgbot.send_file(hmm.chat_id, file=okd, force_document=True, reply_to=okz)
        if os.path.exists(okd):
            os.remove(okd)
    else:
        if "/help" in hmm.text:
            pass
        replied_user = await hmm.client(GetFullUserRequest(hmm.sender_id))
        firstname = replied_user.user.first_name
        vent = hmm.chat_id
        oki = f"**Hey {firstname} !** \n`Send Me A Image Or sticker I Will Resize And Convert To Creatable Sticker It Send It To You` \n**(c) @STARKGANG**"
        await hmm.reply(oki)


@stickertoimgbot.on(events.NewMessage(pattern="^/help$"))
async def search(event):
    await stickertoimgbot.send_file(event.chat_id, file="CAADAgAD6AkAAowucAABsFGHedLEzeUWBA")
    
def resize_image(image, save_locaton):
    """Copyright Rhyse Simpson:
    https://github.com/skittles9823/SkittBot/blob/master/tg_bot/modules/stickers.py
    """
    im = Image.open(image)
    maxsize = (512, 512)
    if (im.width and im.height) < 512:
        size1 = im.width
        size2 = im.height
        if im.width > im.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        im = im.resize(sizenew)
    else:
        im.thumbnail(maxsize)
    file_name = "StickerToImg.png"
    ok = save_locaton + "/" + file_name
    im.save(ok, "PNG")


def is_it_animated_sticker(message):
    try:
        if message.media and message.media.document:
            mime_type = message.media.document.mime_type
            if "tgsticker" in mime_type:
                return True
            else:
                return False
        else:
            return False
    except:
        return False


print("Bot Is Alive.")


def startbot():
    stickertoimgbot.run_until_disconnected()


if __name__ == "__main__":
    startbot()
