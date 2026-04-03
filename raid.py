import asyncio
from random import choice
from telethon import events
from config import SUDO_USERS, OWNER_ID, hl
from AltBots.data import RAID, REPLYRAID, ALTRON, MRAID, SRAID, CRAID

# Global list to track active ReplyRaids across all hosted sessions
REPLY_RAID_LIST = []

def register_raid(client):
    """
    This function attaches all raid handlers to a specific user's client session.
    It preserves all features: Raid, ReplyRaid, MRAID, SRAID, and CRAID.
    """

    # --- STANDARD RAID ---
    @client.on(events.NewMessage(incoming=True, pattern=r"\%sraid(?: |$)(.*)" % hl))
    async def raid(e):
        if e.sender_id in SUDO_USERS:
            xraid = e.text.split(" ", 2)
            uid = None

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
                        reply = choice(RAID)
                        caption = f"{username} {reply}"
                        await e.client.send_message(e.chat_id, caption)
                        await asyncio.sleep(0.1)
            except Exception:
                await e.reply(f"𝗠𝗼𝗱𝘂𝗹𝗲 𝗡𝗮𝗺𝗲: 𝐑𝐚𝐢𝐝\n » {hl}raid <ᴄᴏᴜɴᴛ> <ᴜꜱᴇʀɴᴀᴍᴇ>\n » {hl}raid <ᴄᴏᴜɴᴛ> <ʀᴇᴘʟʏ>")

    # --- REPLY RAID LISTENER ---
    @client.on(events.NewMessage(incoming=True))
    async def reply_raid_listener(event):
        global REPLY_RAID_LIST
        check = f"{event.sender_id}_{event.chat_id}"
        if check in REPLY_RAID_LIST:
            await asyncio.sleep(0.1)
            await event.client.send_message(
                entity=event.chat_id,
                message=choice(REPLYRAID),
                reply_to=event.message.id,
            )

    # --- ACTIVATE REPLY RAID ---
    @client.on(events.NewMessage(incoming=True, pattern=r"\%srraid(?: |$)(.*)" % hl))
    async def rraid(e):
        if e.sender_id in SUDO_USERS:
            mkrr = e.text.split(" ", 1)
            entity = None
            if len(mkrr) == 2:
                entity = await e.client.get_entity(mkrr[1])
            elif e.reply_to_msg_id:             
                a = await e.get_reply_message()
                entity = await e.client.get_entity(a.sender_id)

            if entity:
                user_id = entity.id
                if user_id in ALTRON or user_id == OWNER_ID or user_id in SUDO_USERS:
                    await e.reply("ᴄᴀɴɴᴏᴛ ʀᴀɪᴅ ꜱᴜᴅᴏ/ᴏᴡɴᴇʀ.")
                else:
                    global REPLY_RAID_LIST
                    check = f"{user_id}_{e.chat_id}"
                    if check not in REPLY_RAID_LIST:
                        REPLY_RAID_LIST.append(check)
                    await e.reply("» ᴀᴄᴛɪᴠᴀᴛᴇᴅ ʀᴇᴘʟʏʀᴀɪᴅ !! ✅")

    # --- DEACTIVATE REPLY RAID ---
    @client.on(events.NewMessage(incoming=True, pattern=r"\%sdrraid(?: |$)(.*)" % hl))
    async def drraid(e):
        if e.sender_id in SUDO_USERS:
            text = e.text.split(" ", 1)
            if len(text) == 2:
                entity = await e.client.get_entity(text[1])
            elif e.reply_to_msg_id:             
                a = await e.get_reply_message()
                entity = await e.client.get_entity(a.sender_id)
            
            check = f"{entity.id}_{e.chat_id}"
            global REPLY_RAID_LIST
            if check in REPLY_RAID_LIST:
                REPLY_RAID_LIST.remove(check)
            await e.reply("» ʀᴇᴘʟʏ ʀᴀɪᴅ ᴅᴇ-ᴀᴄᴛɪᴠᴀᴛᴇᴅ !! ✅")

    # --- MRAID (LOVE RAID) ---
    @client.on(events.NewMessage(incoming=True, pattern=r"\%smraid(?: |$)(.*)" % hl))
    async def mraid_cmd(e):
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
                first_name = entity.first_name
                counter = int(xraid[1])
                username = f"[{first_name}](tg://user?id={uid})"
                for _ in range(counter):
                    await e.client.send_message(e.chat_id, f"{username} {choice(MRAID)}")
                    await asyncio.sleep(0.1)
            except Exception:
                await e.reply(f"Usage: {hl}mraid <count> <user>")

    # --- SRAID (SHAYARI RAID) ---
    @client.on(events.NewMessage(incoming=True, pattern=r"\%ssraid(?: |$)(.*)" % hl))
    async def sraid_cmd(e):
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
                first_name = entity.first_name
                counter = int(xraid[1])
                username = f"[{first_name}](tg://user?id={uid})"
                for _ in range(counter):
                    await e.client.send_message(e.chat_id, f"{username} {choice(SRAID)}")
                    await asyncio.sleep(0.1)
            except Exception:
                await e.reply(f"Usage: {hl}sraid <count> <user>")

    # --- CRAID (ABCD RAID) ---
    @client.on(events.NewMessage(incoming=True, pattern=r"\%scraid(?: |$)(.*)" % hl))
    async def craid_cmd(e):
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
                if uid in ALTRON or uid == OWNER_ID or uid in SUDO_USERS:
                    return await e.reply("ɴᴏ, ᴛʜɪꜱ ɢᴜʏ ɪꜱ ᴘʀᴏᴛᴇᴄᴛᴇᴅ.")
                
                first_name = entity.first_name
                counter = int(xraid[1])
                username = f"[{first_name}](tg://user?id={uid})"
                for _ in range(counter):
                    await e.client.send_message(e.chat_id, f"{username} {choice(CRAID)}")
                    await asyncio.sleep(0.1)
            except Exception:
                await e.reply(f"Usage: {hl}craid <count> <user>")
              
