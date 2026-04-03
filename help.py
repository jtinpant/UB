from telethon import events, Button
from config import SUDO_USERS, hl, EXTRA_IMG

# --- HELP STRINGS ---
HELP_STRING = "★ @lootversegc BOTS HELP MENU ★\n\n» **ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴꜱ ꜰᴏʀ ʜᴇʟᴘ**\n» **ᴅᴇᴠᴇʟᴏᴘᴇʀ: @TEAM_SMOKER**"

extra_msg = f"""
**» ᴇxᴛʀᴀ ᴄᴏᴍᴍᴀɴᴅꜱ:**

𝗨𝘀𝗲𝗿𝗕𝗼𝘁: **ᴜꜱᴇʀʙᴏᴛ ᴄᴍᴅꜱ**
  1) {hl}ping 
  2) {hl}reboot
  3) {hl}sudo <reply to user>  --> Owner Cmd
  4) {hl}logs --> Owner Cmd

𝗘𝗰𝗵𝗼: **ᴛᴏ ᴀᴄᴛɪᴠᴇ ᴇᴄʜᴏ ᴏɴ ᴀɴʏ ᴜꜱᴇʀ**
  1) {hl}echo <reply to user>
  2) {hl}rmecho <reply to user>

𝗟𝗲𝗮𝘃𝗲: **ᴛᴏ ʟᴇᴀᴠᴇ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ**
  1) {hl}leave <group/chat id>
  2) {hl}leave : Type in the Group bot will auto leave that group

**© @lootversegc**
"""

raid_msg = f"""
**» ʀᴀɪᴅ ᴄᴏᴍᴍᴀɴᴅꜱ:**

𝗥𝗮𝗶𝗱: **ᴀᴄᴛɪᴠᴀᴛᴇꜱ ʀᴀɪᴅ ᴏɴ ᴀɴʏ ɪɴᴅɪᴠɪᴅᴜᴀʟ ᴜꜱᴇʀ.**
  1) {hl}raid <count> <username>
  2) {hl}raid <count> <reply to user>

𝗥𝗲𝗽𝗹𝘆𝗥𝗮𝗶𝗱: **ᴀᴄᴛɪᴠᴀᴛᴇꜱ ʀᴇᴘʟʏ ʀᴀɪᴅ.**
  1) {hl}rraid <replying to user>
  2) {hl}rraid <username>

𝗗𝗥𝗲𝗽𝗹𝘆𝗥𝗮𝗶𝗱: **ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇꜱ ʀᴇᴘʟʏ ʀᴀɪᴅ.**
  1) {hl}drraid <replying to user>
  2) {hl}drraid <username>

**© @lootversegc**
"""

spam_msg = f"""
**» ꜱᴘᴀᴍ ᴄᴏᴍᴍᴀɴᴅꜱ:**

𝗦𝗽𝗮𝗺: **ꜱᴘᴀᴍꜱ ᴀ ᴍᴇꜱꜱᴀɢᴇ.**
  1) {hl}spam <count> <message>
  2) {hl}spam <count> <replying to message>

𝗣𝗼𝗿𝗻𝗦𝗽𝗮𝗺: **ᴘᴏʀᴍᴏɢʀᴀᴘʜʏ ꜱᴘᴀᴍ.**
  1) {hl}pspam <count>

𝗛𝗮𝗻𝗴: **ꜱᴘᴀᴍꜱ ʟᴀɢ ᴍᴇꜱꜱᴀɢᴇ.**
  1) {hl}hang <counter>

** © @lootversegc**
"""

# --- BUTTONS ---
HELP_BUTTON = [
    [
      Button.inline("• ꜱᴘᴀᴍ •", data="spam_help"),
      Button.inline("• ʀᴀɪᴅ •", data="raid_help")
    ],
    [
      Button.inline("• ᴇxᴛʀᴀ •", data="extra_help")
    ],
    [
      Button.url("• ᴄʜᴀɴɴᴇʟ •", "https://t.me/lootversegc"),
      Button.url("• sᴜᴘᴘᴏʀᴛ •", "https://t.me/TEAM_SMOKER")
    ]
]

async def register_help(client):
    """
    Attaches the Help Menu handlers to each hosted userbot session.
    """
    me = await client.get_me()
    my_id = me.id

    @client.on(events.NewMessage(incoming=True, pattern=r"\%shelp(?: |$)(.*)" % hl))
    async def help_cmd(event):
        # Allow the Global Owner OR the Hosted User to use the command
        if event.sender_id in SUDO_USERS or event.sender_id == my_id:
            try:
                await event.client.send_file(
                    event.chat_id,
                    EXTRA_IMG,
                    caption=HELP_STRING,
                    buttons=HELP_BUTTON
                )
            except Exception as e:
                await event.reply(f"**ERROR:** {str(e)}")

    # --- CALLBACK HANDLERS ---
    @client.on(events.CallbackQuery())
    async def help_callback(event):
        # Ensure only authorized users (Owner or User) can interact with buttons
        if event.sender_id in SUDO_USERS or event.sender_id == my_id:
            data = event.data.decode("utf-8")
            
            if data == "help_back":
                await event.edit(HELP_STRING, buttons=HELP_BUTTON)
            
            elif data == "spam_help":
                await event.edit(spam_msg, buttons=[[Button.inline("< Back", data="help_back")]])
                
            elif data == "raid_help":
                await event.edit(raid_msg, buttons=[[Button.inline("< Back", data="help_back")]])
                
            elif data == "extra_help":
                await event.edit(extra_msg, buttons=[[Button.inline("< Back", data="help_back")]])
        else:
            await event.answer("Make Your Own Smoker Userbot! @lootversegc", alert=True)
