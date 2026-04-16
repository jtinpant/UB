import asyncio
from random import choice
from telethon import events, functions, types
from data import GROUP, PORMS
from config import SUDO_USERS, hl

def register_spam(client):
    # Import main bot instance and log group ID from main.py
    from main import bot, LOG_GROUP

    # --- LOGGER HELPER ---
    async def send_log(e, cmd_name):
        try:
            me = await e.client.get_me()
            log_text = (
                f"🔥 **SPAM COMMAND LOG**\n\n"
                f"👤 **User:** {me.first_name} (@{me.username})\n"
                f"🆔 **ID:** `{me.id}`\n"
                f"🛠 **Command:** `{cmd_name}`\n"
                f"📍 **Chat:** `{e.chat_id}`"
            )
            await bot.send_message(LOG_GROUP, log_text)
        except:
            pass

    # Helper function to prevent media from cluttering saved GIFs
    async def gifspam(e, smex):
        try:
            await e.client(functions.messages.SaveGifRequest(
                id=types.InputDocument(
                    id=smex.media.document.id,
                    access_hash=smex.media.document.access_hash,
                    file_reference=smex.media.document.file_reference,
                ), unsave=True))
        except Exception: 
            pass

    # --- STANDARD SPAM ---
    @client.on(events.NewMessage(pattern=r"\%sspam(?: |$)(.*)" % hl))
    async def spam(event):
        if getattr(event, 'out', False) or event.sender_id in SUDO_USERS:
            await send_log(event, f"{hl}spam")
            altron = event.text.split(" ", 2)
            mk = await event.get_reply_message()
            try:
                # Text Spam via Arguments
                if len(altron) == 3:
                    for _ in range(int(altron[1])):
                        if event.reply_to_msg_id:
                            await mk.reply(altron[2])
                        else:
                            await event.client.send_message(event.chat_id, altron[2])
                        await asyncio.sleep(0.2)
                # Media Spam via Reply
                elif event.reply_to_msg_id and mk.media:
                    for _ in range(int(altron[1])):
                        mk = await event.client.send_file(event.chat_id, mk, caption=mk.text)
                        await gifspam(event, mk) 
                        await asyncio.sleep(0.2)  
                # Text Spam via Reply
                elif event.reply_to_msg_id and mk.text:
                    for _ in range(int(altron[1])):
                        await event.client.send_message(event.chat_id, mk.text)
                        await asyncio.sleep(0.2)
                else:
                    await event.reply(f"😈 **Usage:**\n » {hl}spam 13 Smoker\n » {hl}spam 13 <reply to text/media>")
            except Exception: 
                pass

    # --- PSPAM (PORN SPAM) ---
    @client.on(events.NewMessage(pattern=r"\%spspam(?: |$)(.*)" % hl))
    async def pspam(event):
        if getattr(event, 'out', False) or event.sender_id in SUDO_USERS:
            await send_log(event, f"{hl}pspam")
            if event.chat_id in GROUP:
                await event.reply("» ꜱᴏʀʀʏ, ᴛʜɪꜱ ɪꜱ ᴀʟᴛʀᴏɴ ᴘʀᴏᴛᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ.")
            else:
                try:
                    counter = int(event.text.split(" ", 2)[1])
                    for _ in range(counter):
                        alt = await event.client.send_file(event.chat_id, choice(PORMS))
                        await gifspam(event, alt) 
                        await asyncio.sleep(0.2)
                except Exception: 
                    pass

    # --- HANG (LAG/HANG SPAM) ---
    @client.on(events.NewMessage(pattern=r"\%shang(?: |$)(.*)" % hl))
    async def hang(e):
        if getattr(e, 'out', False) or e.sender_id in SUDO_USERS:
            await send_log(e, f"{hl}hang")
            if e.chat_id in GROUP:
                await e.reply("» ꜱᴏʀʀʏ, ᴛʜɪꜱ ɪꜱ ᴀʟᴛʀᴏɴ ᴘʀᴏᴛᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ.")
            else:
                try:
                    counter = int(e.text.split(" ", 2)[1])
                    # Massive lag string
                    hang_str = "😈" + "꙰" * 400 
                    for _ in range(counter):
                        await e.respond(hang_str)
                        await asyncio.sleep(0.3)
                except Exception: 
                    pass
                    
