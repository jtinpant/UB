import asyncio
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID
from raid import register_raid
from spam import register_spam
from help import register_help

# Memory-based storage (No Database URL)
GLOBAL_CLIENTS = {}

bot = TelegramClient('SmokerHost', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    welcome = "🔥 **SMOKER USERBOT HOSTING** 🔥\n\nClick below to host your ID."
    buttons = [[Button.inline("🚀 LOGIN", data="login")], [Button.url("📢 CHANNEL", "https://t.me/TEAM_SMOKER")]]
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
            await client.sign_in(phone, code=otp)
            
            # Start and Register
            register_raid(client)
            register_spam(client)
            register_help(client)
            
            GLOBAL_CLIENTS[event.sender_id] = client
            await conv.send_message("✅ **Hosted successfully!**")
        except Exception as e:
            await conv.send_message(f"❌ Error: {str(e)}")

@bot.on(events.NewMessage(pattern='/logout'))
async def logout(event):
    if event.sender_id in GLOBAL_CLIENTS:
        await GLOBAL_CLIENTS[event.sender_id].disconnect()
        del GLOBAL_CLIENTS[event.sender_id]
        await event.respond("🚫 **Logged out successfully.**")
    else:
        await event.respond("You have no active session.")

if __name__ == "__main__":
    bot.run_until_disconnected()
        try:
            await conv.send_message("📱 Please send your **Phone Number** with country code (e.g., +919876543210):")
            phone = (await conv.get_response()).text
            
            # Start temporary client for login
            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()
            
            sent_code = await client.send_code_request(phone)
            await conv.send_message("📩 **OTP Sent!** Please send the OTP in this format: `1 2 3 4 5` (spaces between numbers)")
            otp = (await conv.get_response()).text.replace(" ", "")
            
            try:
                await client.sign_in(phone, code=otp)
            except SessionPasswordNeededError:
                await conv.send_message("🔐 **2-Step Verification** is enabled. Please send your password:")
                password = (await conv.get_response()).text
                await client.sign_in(password=password)
            
            # Successful Login
            session_str = client.session.save()
            HOSTED_SESSIONS[sender] = session_str
            
            # Register all your commands to this new session
            register_raid(client)
            register_spam(client)
            register_help(client)
            
            await conv.send_message("✅ **SUCCESS!** Your ID is now hosted on SMOKER USERBOT.\nSend `.help` in any chat to begin.")
            
        except Exception as e:
            await conv.send_message(f"❌ **FAILED:** {str(e)}")

# --- LOGOUT ---
@bot.on(events.NewMessage(pattern='/logout'))
async def logout(event):
    user_id = event.sender_id
    if user_id in HOSTED_SESSIONS:
        del HOSTED_SESSIONS[user_id]
        await event.respond("🚫 **LOGGED OUT:** Your session has been removed from our hosting.")
    else:
        await event.respond("You don't have any active session hosted.")

# --- OWNER CONTROL ---
@bot.on(events.NewMessage(pattern='/stats'))
async def stats(event):
    if event.sender_id == OWNER_ID:
        total = len(HOSTED_SESSIONS)
        await event.respond(f"📊 **TOTAL USERS HOSTING:** {total}")

if __name__ == "__main__":
    print("Smoker Userbot Hosting Started...")
    bot.run_until_disconnected()
              
