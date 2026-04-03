import asyncio
from random import choice
from telethon import events, functions, types
from data import GROUP, PORMS # Updated import
from config import SUDO_USERS, hl

def register_spam(client):
    async def gifspam(e, smex):
        try:
            await e.client(functions.messages.SaveGifRequest(
                id=types.InputDocument(
                    id=smex.media.document.id,
                    access_hash=smex.media.document.access_hash,
                    file_reference=smex.media.document.file_reference,
                ), unsave=True))
        except Exception: pass

    @client.on(events.NewMessage(incoming=True, pattern=r"\%sspam(?: |$)(.*)" % hl))
    async def spam(event):
        if event.sender_id in SUDO_USERS:
            altron = event.text.split(" ", 2)
            mk = await event.get_reply_message()
            try:
                if len(altron) == 3:
                    for _ in range(int(altron[1])):
                        await mk.reply(altron[2]) if event.reply_to_msg_id else await event.client.send_message(event.chat_id, altron[2])
                        await asyncio.sleep(0.2)
                elif event.reply_to_msg_id and mk.media:
                    for _ in range(int(altron[1])):
                        mk = await event.client.send_file(event.chat_id, mk, caption=mk.text)
                        await gifspam(event, mk)
                        await asyncio.sleep(0.2)
            except Exception: pass

    @client.on(events.NewMessage(incoming=True, pattern=r"\%spspam(?: |$)(.*)" % hl))
    async def pspam(event):
        if event.sender_id in SUDO_USERS:
            if event.chat_id in GROUP:
                await event.reply("» ꜱᴏʀʀʏ, ᴛʜɪꜱ ɪꜱ ᴀʟᴛʀᴏɴ ᴘʀᴏᴛᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ.")
            else:
                try:
                    counter = int(event.text.split(" ", 2)[1])
                    for _ in range(counter):
                        alt = await event.client.send_file(event.chat_id, choice(PORMS))
                        await gifspam(event, alt)
                        await asyncio.sleep(0.2)
                except Exception: pass

    @client.on(events.NewMessage(incoming=True, pattern=r"\%shang(?: |$)(.*)" % hl))
    async def hang(e):
        if e.sender_id in SUDO_USERS:
            if e.chat_id in GROUP:
                await e.reply("» ꜱᴏʀʀʏ, ᴛʜɪꜱ ɪꜱ ᴀʟᴛʀᴏɴ ᴘʀᴏᴛᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ.")
            else:
                try:
                    counter = int(e.text.split(" ", 2)[1])
                    # This uses the specialized hanging string from your original file
                    hang_str = "😈" + "꙰" * 400 
                    for _ in range(counter):
                        await e.respond(hang_str)
                        await asyncio.sleep(0.3)
                except Exception: pass
