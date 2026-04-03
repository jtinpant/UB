import asyncio
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID
from raid import register_raid
from spam import register_spam
from help import register_help

GLOBAL_CLIENTS = {}
bot = TelegramClient('SmokerHost', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    welcome = "🔥 **SMOKER USERBOT HOSTING** 🔥\n\nClick below to host your ID."
    buttons = [
        [Button.inline("🚀 LOGIN", data="login")],
        [
            Button.url("❤️‍🔥 OWNER ❄️", "https://t.me/Divyansh6565"),
            Button.url("📢 CHANNEL", "https://t.me/lootversegc")
        ]
    ]
    await event.respond(welcome, buttons=buttons)

@bot.on(events.CallbackQuery(data="login"))
async def login_handler(event):
    async with bot.conversation(event.sender_id) as conv:
        try:
            await conv.send_message("📱 Send your **Phone Number** (+91...):")
            phone = (await conv.get_response()).text
            
            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()
            await client.send_code_request(phone)
            
            await conv.send_message("📩 Send **OTP** (e.g., 1 2 3 4 5):")
            otp = (await conv.get_response()).text.replace(" ", "")
            
            try:
                await client.sign_in(phone, code=otp)
            except SessionPasswordNeededError:
                await conv.send_message("🔐 **2FA Enabled.** Send your password:")
                password = (await conv.get_response()).text
                await client.sign_in(password=password)
            
            # FIXED: Removed 'await' so it doesn't crash with NoneType
            register_raid(client)
            register_spam(client)
            register_help(client)
            
            GLOBAL_CLIENTS[event.sender_id] = client
            await conv.send_message("✅ **Hosted successfully!** Try sending `.help` now.")
            
        except Exception as e:
            await conv.send_message(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    bot.run_until_disconnected()
            otp = (await conv.get_response()).text.replace(" ", "")
            
            try:
                await client.sign_in(phone, code=otp)
            except SessionPasswordNeededError:
                await conv.send_message("🔐 **2FA Enabled.** Send your password:")
                password = (await conv.get_response()).text
                await client.sign_in(password=password)
            
            # --- IMPORTANT: ADD AWAIT HERE ---
            await register_raid(client)
            await register_spam(client)
            await register_help(client)
            
            GLOBAL_CLIENTS[event.sender_id] = client
            await conv.send_message("✅ **Hosted successfully!** Try sending `.help` now.")
            
        except Exception as e:
            await conv.send_message(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("Smoker Userbot Hosting is live...")
    bot.run_until_disconnected()
    
