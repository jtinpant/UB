from telethon import events, functions, types
from config import SUDO_USERS, hl
import asyncio
import os

# Global storage for revert functionality
original_data = {}
mute_list = []

def register_extra(client):

    # --- BAN ALL ---
    @client.on(events.NewMessage(pattern=r"\%sbanall$" % hl))
    async def banall(event):
        if getattr(event, 'out', False) or event.sender_id in SUDO_USERS:
            if event.is_group:
                await event.reply("🚫 **Banning all members...**")
                async for user in event.client.iter_participants(event.chat_id):
                    if not user.is_self and not user.is_bot:
                        try:
                            await event.client.edit_permissions(event.chat_id, user.id, view_messages=False)
                        except: continue
                await event.delete()

    # --- UNBAN ALL ---
    @client.on(events.NewMessage(pattern=r"\%sunbanall$" % hl))
    async def unbanall(event):
        if getattr(event, 'out', False) or event.sender_id in SUDO_USERS:
            if event.is_group:
                await event.reply("✅ **Unbanning all members...**")
                async for user in event.client.iter_participants(event.chat_id, filter=types.ChannelParticipantsKicked):
                    try:
                        await event.client.edit_permissions(event.chat_id, user.id, view_messages=True)
                    except: continue

    # --- MUTE USER ---
    @client.on(events.NewMessage(pattern=r"\%smute(?: |$)(.*)" % hl))
    async def mute(event):
        if getattr(event, 'out', False) or event.sender_id in SUDO_USERS:
            target = event.pattern_match.group(1) or (await event.get_reply_message()).sender_id
            user = await event.client.get_entity(target)
            mute_list.append(user.id)
            await event.reply(f"🔇 **Muted:** {user.first_name}. All their messages will be deleted.")

    @client.on(events.NewMessage())
    async def mute_handler(event):
        if event.sender_id in mute_list:
            await event.delete()

    @client.on(events.NewMessage(pattern=r"\%sunmute" % hl))
    async def unmute(event):
        if getattr(event, 'out', False) or event.sender_id in SUDO_USERS:
            user = await event.get_reply_message()
            if user and user.sender_id in mute_list:
                mute_list.remove(user.sender_id)
                await event.reply("🔊 **User Unmuted.**")

    # --- BROADCAST ---
    @client.on(events.NewMessage(pattern=r"\%sbroadcast" % hl))
    async def broadcast(event):
        if getattr(event, 'out', False) or event.sender_id in SUDO_USERS:
            msg = await event.get_reply_message()
            await event.reply("📢 **Broadcasting...**")
            async for dialog in event.client.iter_dialogs():
                try:
                    if dialog.is_group or dialog.is_user:
                        await event.client.send_message(dialog.id, msg)
                        await asyncio.sleep(0.5)
                except: continue
            await event.reply("✅ **Broadcast complete.**")

    # --- INFO ---
    @client.on(events.NewMessage(pattern=r"\%sinfo(?: |$)(.*)" % hl))
    async def info(event):
        if getattr(event, 'out', False) or event.sender_id in SUDO_USERS:
            target = event.pattern_match.group(1) or (await event.get_reply_message()).sender_id
            user = await event.client.get_entity(target)
            full_user = await event.client(functions.users.GetFullUserRequest(user.id))
            info_text = (
                f"👤 **USER INFO**\n\n"
                f"• **Name:** {user.first_name} {user.last_name or ''}\n"
                f"• **Username:** @{user.username or 'None'}\n"
                f"• **ID:** `{user.id}`\n"
                f"• **Bio:** {full_user.full_user.about or 'None'}"
            )
            await event.reply(info_text)

    # --- CLONE ---
    @client.on(events.NewMessage(pattern=r"\%sclone(?: |$)(.*)" % hl))
    async def clone(event):
        if getattr(event, 'out', False) or event.sender_id in SUDO_USERS:
            target = event.pattern_match.group(1) or (await event.get_reply_message()).sender_id
            user = await event.client.get_entity(target)
            full_user = await event.client(functions.users.GetFullUserRequest(user.id))
            me = await event.client.get_me()
            
            # Fix: Save current state to original_data
            original_data['first_name'] = me.first_name
            original_data['last_name'] = me.last_name or ''
            original_data['bio'] = (await event.client(functions.users.GetFullUserRequest('me'))).full_user.about
            
            await event.client(functions.account.UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name or ''))
            await event.client(functions.account.UpdateProfileRequest(about=full_user.full_user.about))
            
            photos = await event.client.get_profile_photos(user.id)
            if photos:
                path = await event.client.download_media(photos[0])
                file = await event.client.upload_file(path)
                await event.client(functions.photos.UploadProfilePhotoRequest(file=file))
                os.remove(path)
                
            await event.reply("✅ **Cloned successfully!**")

    # --- REVERT ---
    @client.on(events.NewMessage(pattern=r"\%srevert$" % hl))
    async def revert(event):
        if getattr(event, 'out', False) or event.sender_id in SUDO_USERS:
            if 'first_name' in original_data:
                await event.client(functions.account.UpdateProfileRequest(
                    first_name=original_data['first_name'], 
                    last_name=original_data['last_name']
                ))
                await event.client(functions.account.UpdateProfileRequest(about=original_data['bio']))
                await event.reply("✅ **Reverted to original profile!**")
            else:
                await event.reply("❌ **No clone data found to revert.**")

    # --- HELP ---
    @client.on(events.NewMessage(pattern=r"\%shelp$" % hl))
    async def help_cmd(event):
        if getattr(event, 'out', False) or event.sender_id in SUDO_USERS:
            help_text = (
                "🤖 **SMOKER USERBOT - FULL COMMAND LIST** 🤖\n\n"
                "**☠️ SPAM & RAID:**\n"
                f"• `{hl}spam` : Spam message 💀\n"
                f"• `{hl}pspam` : Porn spam 🔞\n"
                f"• `{hl}hang` : Hang string spam 🧨\n"
                f"• `{hl}raid` : Raid target 💣\n"
                f"• `{hl}rraid` : Reply raid ☣️\n"
                f"• `{hl}drraid` : Disable reply raid ⚠️\n"
                f"• `{hl}mraid` : Shayari raid 🥀\n"
                f"• `{hl}sraid` : Love raid 💔\n"
                f"• `{hl}craid` : ABCD raid 🔤\n\n"
                "**🔥 ADMIN & EXTRA:**\n"
                f"• `{hl}banall` : Nuke group 🚫\n"
                f"• `{hl}unbanall` : Unban all ✅\n"
                f"• `{hl}mute` : Delete user msgs 🔇\n"
                f"• `{hl}unmute` : Stop deleting 🔊\n"
                f"• `{hl}broadcast` : Global broadcast 📢\n"
                f"• `{hl}info` : User info 🆔\n"
                f"• `{hl}clone` : Profile clone 🎭\n"
                f"• `{hl}revert` : Restore profile 🔙"
            )
            await event.reply(help_text)
          
