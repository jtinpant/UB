import asyncio
from random import choice
from telethon import events
from data import RAID, REPLYRAID, ALTRON, MRAID, SRAID, CRAID 
from config import SUDO_USERS, OWNER_ID, hl

def register_raid(client):
    # UNIQUE LIST FOR EACH HOSTED CLIENT
    # This ensures User A's raid list is separated from User B's raid list
    reply_raid_list = []

    # --- STANDARD RAID ---
    @client.on(events.NewMessage(pattern=r"\%sraid(?: |$)(.*)" % hl))
    async def raid(e):
        if getattr(e, 'out', False) or e.sender_id in SUDO_USERS:
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
                if uid in ALTRON or uid == OWNER_ID or uid in SUDO_USERS:
                    await e.reply("ɴᴏ, ᴛʜɪꜱ ɢᴜʏ ɪꜱ ᴘʀᴏᴛᴇᴄᴛᴇᴅ.")
                else:
                    first_name = getattr(entity, 'first_name', 'User')
                    counter = int(xraid[1])
                    username = f"[{first_name}](tg://user?id={uid})"
                    for _ in range(counter):
                        await e.client.send_message(e.chat_id, f"{username} {choice(RAID)}")
                        await asyncio.sleep(0.1)
            except Exception:
                await e.reply(f"Usage: {hl}raid <count> <username> OR {hl}raid <count> <reply>")

    # --- REPLY RAID LISTENER ---
    @client.on(events.NewMessage())
    async def reply_raid_exec(event):
        # Checks the unique list for THIS specific client only
        check = f"{event.sender_id}_{event.chat_id}"
        if check in reply_raid_list:
            await asyncio.sleep(0.1)
            await event.client.send_message(event.chat_id, choice(REPLYRAID), reply_to=event.message.id)

    # --- ACTIVATE REPLY RAID ---
    @client.on(events.NewMessage(pattern=r"\%srraid(?: |$)(.*)" % hl))
    async def rraid(e):
        if getattr(e, 'out', False) or e.sender_id in SUDO_USERS:
            mkrr = e.text.split(" ", 1)
            entity = await e.client.get_entity(mkrr[1]) if len(mkrr) == 2 else await e.get_reply_message()
            user_id = entity.id if len(mkrr) == 2 else entity.sender_id
            
            if user_id in ALTRON or user_id == OWNER_ID or user_id in SUDO_USERS:
                await e.reply("ɴᴏ, ᴛʜɪꜱ ɢᴜʏ ɪꜱ ᴘʀᴏᴛᴇᴄᴛᴇᴅ.")
            else:
                check = f"{user_id}_{e.chat_id}"
                if check not in reply_raid_list: 
                    reply_raid_list.append(check)
                await e.reply("» ᴀᴄᴛɪᴠᴀᴛᴇᴅ ʀᴇᴘʟʏʀᴀɪᴅ !! ✅")

    # --- DEACTIVATE REPLY RAID ---
    @client.on(events.NewMessage(pattern=r"\%sdrraid(?: |$)(.*)" % hl))
    async def drraid(e):
        if getattr(e, 'out', False) or e.sender_id in SUDO_USERS:
            text = e.text.split(" ", 1)
            entity = await e.client.get_entity(text[1]) if len(text) == 2 else await e.get_reply_message()
            user_id = entity.id if len(text) == 2 else entity.sender_id
            
            check = f"{user_id}_{e.chat_id}"
            if check in reply_raid_list: 
                reply_raid_list.remove(check)
            await e.reply("» ʀᴇᴘʟʏ ʀᴀɪᴅ ᴅᴇ-ᴀᴄᴛɪᴠᴀᴛᴇᴅ !! ✅")

    # --- MRAID (LOVE RAID) ---
    @client.on(events.NewMessage(pattern=r"\%smraid(?: |$)(.*)" % hl))
    async def mraid_cmd(e):
        if getattr(e, 'out', False) or e.sender_id in SUDO_USERS:
            xraid = e.text.split(" ", 2)
            entity = await e.client.get_entity(xraid[2]) if len(xraid) == 3 else await e.get_reply_message()
            uid = entity.id if len(xraid) == 3 else entity.sender_id
            try:
                counter = int(xraid[1])
                first_name = getattr(entity, 'first_name', 'User')
                username = f"[{first_name}](tg://user?id={uid})"
                for _ in range(counter):
                    await e.client.send_message(e.chat_id, f"{username} {choice(MRAID)}")
                    await asyncio.sleep(0.1)
            except Exception:
                await e.reply(f"Usage: {hl}mraid <count> <username> OR {hl}mraid <count> <reply>")

    # --- SRAID (SHAYARI RAID) ---
    @client.on(events.NewMessage(pattern=r"\%ssraid(?: |$)(.*)" % hl))
    async def sraid_cmd(e):
        if getattr(e, 'out', False) or e.sender_id in SUDO_USERS:
            xraid = e.text.split(" ", 2)
            entity = await e.client.get_entity(xraid[2]) if len(xraid) == 3 else await e.get_reply_message()
            uid = entity.id if len(xraid) == 3 else entity.sender_id
            try:
                counter = int(xraid[1])
                first_name = getattr(entity, 'first_name', 'User')
                username = f"[{first_name}](tg://user?id={uid})"
                for _ in range(counter):
                    await e.client.send_message(e.chat_id, f"{username} {choice(SRAID)}")
                    await asyncio.sleep(0.1)
            except Exception:
                await e.reply(f"Usage: {hl}sraid <count> <username> OR {hl}sraid <count> <reply>")

    # --- CRAID (ABCD RAID) ---
    @client.on(events.NewMessage(pattern=r"\%scraid(?: |$)(.*)" % hl))
    async def craid_cmd(e):
        if getattr(e, 'out', False) or e.sender_id in SUDO_USERS:
            xraid = e.text.split(" ", 2)
            entity = await e.client.get_entity(xraid[2]) if len(xraid) == 3 else await e.get_reply_message()
            uid = entity.id if len(xraid) == 3 else entity.sender_id
            try:
                if uid in ALTRON or uid == OWNER_ID or uid in SUDO_USERS:
                    return await e.reply("ɴᴏ, ᴛʜɪꜱ ɢᴜʏ ɪꜱ ᴘʀᴏᴛᴇᴄᴛᴇᴅ.")
                
                counter = int(xraid[1])
                first_name = getattr(entity, 'first_name', 'User')
                username = f"[{first_name}](tg://user?id={uid})"
                for _ in range(counter):
                    await e.client.send_message(e.chat_id, f"{username} {choice(CRAID)}")
                    await asyncio.sleep(0.1)
            except Exception:
                await e.reply(f"Usage: {hl}craid <count> <username> OR {hl}craid <count> <reply>")
                
