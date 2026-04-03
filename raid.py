import asyncio
from random import choice
from telethon import events
# Updated import to match your current repo structure
from data import RAID, REPLYRAID, ALTRON, MRAID, SRAID, CRAID 
from config import SUDO_USERS, OWNER_ID, hl

REPLY_RAID_LIST = []

def register_raid(client):
    @client.on(events.NewMessage(incoming=True, pattern=r"\%sraid(?: |$)(.*)" % hl))
    async def raid(e):
        if e.sender_id in SUDO_USERS:
            xraid = e.text.split(" ", 2)
            if len(xraid) == 3:
                entity = await e.client.get_entity(xraid[2])
                uid = entity.id
            elif e.reply_to_msg_id:             
                a = await e.get_reply_message()
                entity = await e.client.get_entity(a.sender_id)
                uid = entity.id
            try:
                if uid in ALTRON:
                    await e.reply("ɴᴏ, ᴛʜɪꜱ ɢᴜʏ ɪꜱ ᴀʟᴛʀᴏɴ'ꜱ ᴏᴡɴᴇʀ.")
                elif uid == OWNER_ID:
                    await e.reply("ɴᴏ, ᴛʜɪꜱ ɢᴜʏ ɪꜱ ᴏᴡɴᴇʀ ᴏꜰ ᴛʜᴇꜱᴇ ʙᴏᴛꜱ.")
                elif uid in SUDO_USERS:
                    await e.reply("ɴᴏ, ᴛʜɪꜱ ɢᴜʏ ɪꜱ ᴀ ꜱᴜᴅᴏ ᴜꜱᴇʀ.")
                else:
                    first_name = entity.first_name
                    counter = int(xraid[1])
                    username = f"[{first_name}](tg://user?id={uid})"
                    for _ in range(counter):
                        await e.client.send_message(e.chat_id, f"{username} {choice(RAID)}")
                        await asyncio.sleep(0.1)
            except Exception:
                await e.reply(f"𝗠𝗼𝗱𝘂𝗹𝗲 𝗡𝗮𝗺𝗲: 𝐑𝐚𝐢𝐝\n » {hl}raid <ᴄᴏᴜɴᴛ> <ᴜꜱᴇʀ>\n » {hl}raid <ᴄᴏᴜɴᴛ> <ʀᴇᴘʟʏ>")

    @client.on(events.NewMessage(incoming=True))
    async def reply_raid_exec(event):
        global REPLY_RAID_LIST
        check = f"{event.sender_id}_{event.chat_id}"
        if check in REPLY_RAID_LIST:
            await asyncio.sleep(0.1)
            await event.client.send_message(event.chat_id, choice(REPLYRAID), reply_to=event.message.id)

    @client.on(events.NewMessage(incoming=True, pattern=r"\%srraid(?: |$)(.*)" % hl))
    async def rraid(e):
        if e.sender_id in SUDO_USERS:
            mkrr = e.text.split(" ", 1)
            entity = await e.client.get_entity(mkrr[1]) if len(mkrr) == 2 else await e.get_reply_message()
            user_id = entity.id if len(mkrr) == 2 else entity.sender_id
            if user_id not in SUDO_USERS and user_id != OWNER_ID:
                global REPLY_RAID_LIST
                check = f"{user_id}_{e.chat_id}"
                if check not in REPLY_RAID_LIST: REPLY_RAID_LIST.append(check)
                await e.reply("» ᴀᴄᴛɪᴠᴀᴛᴇᴅ ʀᴇᴘʟʏʀᴀɪᴅ !! ✅")

    @client.on(events.NewMessage(incoming=True, pattern=r"\%sdrraid(?: |$)(.*)" % hl))
    async def drraid(e):
        if e.sender_id in SUDO_USERS:
            text = e.text.split(" ", 1)
            entity = await e.client.get_entity(text[1]) if len(text) == 2 else await e.get_reply_message()
            user_id = entity.id if len(text) == 2 else entity.sender_id
            check = f"{user_id}_{e.chat_id}"
            global REPLY_RAID_LIST
            if check in REPLY_RAID_LIST: REPLY_RAID_LIST.remove(check)
            await e.reply("» ʀᴇᴘʟʏ ʀᴀɪᴅ ᴅᴇ-ᴀᴄᴛɪᴠᴀᴛᴇᴅ !! ✅")

    @client.on(events.NewMessage(incoming=True, pattern=r"\%smraid(?: |$)(.*)" % hl))
    async def mraid(e):
        if e.sender_id in SUDO_USERS:
            # logic for MRAID from your data.py
            pass # (similar structure to standard raid using MRAID list)
