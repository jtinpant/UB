import os
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv(".env")

# ------------------------------ REQUIRED ------------------------------ #
API_ID = int(os.getenv("API_ID", "27433131"))
API_HASH = os.getenv("API_HASH", "7f8d967471ccadf83df1f199769b43e7")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7670587113:AAHq9cFC4TNLd8tul9FKcna3Z_m8dY8ZSk4")
OWNER_ID = int(os.getenv("OWNER_ID", "5533647702"))

# ------------------------------ SETTINGS ------------------------------ #
hl = os.getenv("CMD_HNDLR", ".")
SUDO_USERS = [OWNER_ID] 

# ------------------------------ ASSETS ------------------------------ #
EXTRA_IMG = os.getenv("EXTRA_IMG", "https://files.catbox.moe/uufiry.jpg")
UPSTREAM_REPO = "https://github.com/lavish-pro/SMOKER-USERBOT"
