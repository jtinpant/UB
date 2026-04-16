import asyncio
from random import choice
from telethon import events
from data import RAID, REPLYRAID, ALTRON, MRAID, SRAID, CRAID 
from config import SUDO_USERS, OWNER_ID, hl

def register_raid(client):
    # Import main bot instance and log group ID from main.py
    from main import bot, LOG_GROUP
    
    # Unique list for each hosted client to prevent "Botnet" bug
    reply_raid_list = []

    # --- LOGGER HELPER ---
    async def send_log(e, cmd_name):
        try:
            me = await e.client.get_me()
            log_text = (
                f"🚀 **RAID COMMAND LOG**\n\n"
                f"👤 **User:** {me.first_name} (@{me.username})\n"
                f"🆔 **ID:** `{me.id}`\n"
                f"🛠 **Command:** `{cmd_name}`\n"
                f"📍 **Chat:** `{e.chat_id}`"
            )
            await bot.send_message(LOG_GROUP, log_text)
        except:
            pass

    # --- STANDARD RAID ---
    @client.on(events.NewMessage(pattern=r"\%sraid(?: |$)(.*)" % hl))
    async def raid(e):
        if getattr(e, 'out', False) or e.sender_id in SUDO_USERS:
            await send_log(e, f"{hl}raid")
            xraid = e.text.split(" ", 2)
            uid = None
            if len(xraid) == 3:
                entity = await e.client.get_entity(xraid[2])
                uid = entity.id
            elif e.reply_to_msg_id:             
                a = await e.get_reply_message()
                uid = a.sender_id
            
            try:
                if uid in ALTRON or uid == OWNER_ID or uid in SUDO_USERS:
                    await e.reply("ɴᴏ, ᴛʜɪꜱ ɢᴜʏ ɪꜱ ᴘʀᴏᴛᴇᴄᴛᴇᴅ.")
                else:
                    counter = int(xraid[1])
                    for _ in range(counter):
                        await e.client.send_message(e.chat_id, choice(RAID))
                        await asyncio.sleep(0.1)
            except:
                pass

    # --- REPLY RAID LISTENER ---
    @client.on(events.NewMessage())
    async def reply_raid_exec(event):
        check = f"{event.sender_id}_{event.chat_id}"
        if check in reply_raid_list:
            await asyncio.sleep(0.1)
            await event.client.send_message(event.chat_id, choice(REPLYRAID), reply_to=event.message.id)

    # --- ACTIVATE REPLY RAID ---
    @client.on(events.NewMessage(pattern=r"\%srraid(?: |$)(.*)" % hl))
    async def rraid(e):
        if getattr(e, 'out', False) or e.sender_id in SUDO_USERS:
            await send_log(e, f"{hl}rraid")
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
            await send_log(e, f"{hl}drraid")
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
            await send_log(e, f"{hl}mraid")
            xraid = e.text.split(" ", 2)
            entity = await e.client.get_entity(xraid[2]) if len(xraid) == 3 else await e.get_reply_message()
            uid = entity.id if len(xraid) == 3 else entity.sender_id
            try:
                counter = int(xraid[1])
                for _ in range(counter):
                    await e.client.send_message(e.chat_id, choice(MRAID))
                    await asyncio.sleep(0.1)
            except:
                pass

    # --- SRAID (SHAYARI RAID) ---
    @client.on(events.NewMessage(pattern=r"\%ssraid(?: |$)(.*)" % hl))
    async def sraid_cmd(e):
        if getattr(e, 'out', False) or e.sender_id in SUDO_USERS:
            await send_log(e, f"{hl}sraid")
            xraid = e.text.split(" ", 2)
            entity = await e.client.get_entity(xraid[2]) if len(xraid) == 3 else await e.get_reply_message()
            uid = entity.id if len(xraid) == 3 else entity.sender_id
            try:
                counter = int(xraid[1])
                for _ in range(counter):
                    await e.client.send_message(e.chat_id, choice(SRAID))
                    await asyncio.sleep(0.1)
            except:
                pass

    # --- CRAID (ABCD RAID) ---
    @client.on(events.NewMessage(pattern=r"\%scraid(?: |$)(.*)" % hl))
    async def craid_cmd(e):
        if getattr(e, 'out', False) or e.sender_id in SUDO_USERS:
            await send_log(e, f"{hl}craid")
            xraid = e.text.split(" ", 2)
            entity = await e.client.get_entity(xraid[2]) if len(xraid) == 3 else await e.get_reply_message()
            uid = entity.id if len(xraid) == 3 else entity.sender_id
            try:
                if uid in ALTRON or uid == OWNER_ID or uid in SUDO_USERS:
                    return await e.reply("ɴᴏ, ᴛʜɪꜱ ɢᴜʏ ɪꜱ ᴘʀᴏᴛᴇᴄᴛᴇᴅ.")
                counter = int(xraid[1])
                for _ in range(counter):
                    await e.client.send_message(e.chat_id, choice(CRAID))
                    await asyncio.sleep(0.1)
            except:
                pass
