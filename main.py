import asyncio
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID
from raid import register_raid
from spam import register_spam
from help import register_help

# Memory-based storage for active sessions (No Database URL)
GLOBAL_CLIENTS = {}

# Initialize the Main Bot using your provided token
bot = TelegramClient('SmokerHost', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

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

@bot.on(events.CallbackQuery(data="login"))
async def login_handler(event):
    async with bot.conversation(event.sender_id) as conv:
        try:
            await conv.send_message("📱 Please send your **Phone Number** with country code (e.g., +919876543210):")
            phone_res = await conv.get_response()
            phone = phone_res.text
            
            # Start temporary client for login process
            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()
            await client.send_code_request(phone)
            
            await conv.send_message("📩 **OTP Sent!** Please send the OTP in this format: `1 2 3 4 5` (spaces between numbers)")
            otp_res = await conv.get_response()
            otp = otp_res.text.replace(" ", "")
            
            await client.sign_in(phone, code=otp)
            
            # Register modules for the newly hosted session
            register_raid(client)
            register_spam(client)
            register_help(client)
            
            # Store the active client in memory
            GLOBAL_CLIENTS[event.sender_id] = client
            await conv.send_message("✅ **Hosted successfully!** Your Userbot is now active. Send `.help` in any chat to begin.")
            
        except Exception as e:
            await conv.send_message(f"❌ **Error during login:** {str(e)}")

@bot.on(events.NewMessage(pattern='/logout'))
async def logout(event):
    if event.sender_id in GLOBAL_CLIENTS:
        await GLOBAL_CLIENTS[event.sender_id].disconnect()
        del GLOBAL_CLIENTS[event.sender_id]
        await event.respond("🚫 **Logged out successfully.** Your session has been removed from the hosting.")
    else:
        await event.respond("You do not have an active session currently hosted.")

if __name__ == "__main__":
    print("Smoker Userbot Hosting is now live...")
    bot.run_until_disconnected()
