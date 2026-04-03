import asyncio
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID
from raid import register_raid
from spam import register_spam
from help import register_help

# Memory-based storage for active sessions
GLOBAL_CLIENTS = {}

# Initialize the Main Bot
bot = TelegramClient('SmokerHost', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    welcome = "🔥 **SMOKER USERBOT HOSTING** 🔥\n\nClick below to host your ID."
    buttons = [
        [Button.inline("🚀 LOGIN", data="login")],
        [Button.url("📢 CHANNEL", "https://t.me/TEAM_SMOKER")]
    ]
    await event.respond(welcome, buttons=buttons)

@bot.on(events.CallbackQuery(data="login"))
async def login_handler(event):
    async with bot.conversation(event.sender_id) as conv:
        try:
            await conv.send_message("📱 Send your **Phone Number** (+91...):")
            phone_res = await conv.get_response()
            phone = phone_res.text
            
            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()
            await client.send_code_request(phone)
            
            await conv.send_message("📩 Send **OTP** (e.g., 1 2 3 4 5):")
            otp_res = await conv.get_response()
            otp = otp_res.text.replace(" ", "")
            
            await client.sign_in(phone, code=otp)
            
            # Start and Register Modules
            register_raid(client)
            register_spam(client)
            register_help(client)
            
            GLOBAL_CLIENTS[event.sender_id] = client
            await conv.send_message("✅ **Hosted successfully!** Your Userbot is now active.")
            
        except Exception as e:
            await conv.send_message(f"❌ **Error:** {str(e)}")

@bot.on(events.NewMessage(pattern='/logout'))
async def logout(event):
    if event.sender_id in GLOBAL_CLIENTS:
        await GLOBAL_CLIENTS[event.sender_id].disconnect()
        del GLOBAL_CLIENTS[event.sender_id]
        await event.respond("🚫 **Logged out successfully.** Session removed.")
    else:
        await event.respond("You have no active session.")

if __name__ == "__main__":
    print("Smoker Userbot is running...")
    bot.run_until_disconnected()
