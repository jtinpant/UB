import os
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv(".env")

# ------------------------------ REQUIRED ------------------------------ #

API_ID = int(os.getenv("API_ID", "27433131"))
API_HASH = os.getenv("API_HASH", "7f8d967471ccadf83df1f199769b43e7")

# Your New Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "8579256317:AAGH40uDAKZXyW8rxDa-n0Sp5NGkUPaw5-4")

# Your New Owner ID
OWNER_ID = int(os.getenv("OWNER_ID", "5533647702"))

# ------------------------------ SETTINGS ------------------------------ #

hl = os.getenv("CMD_HNDLR", ".")

SUDO_USERS = [OWNER_ID] # Owner is automatically sudo

# ------------------------------ ASSETS ------------------------------ #

EXTRA_IMG = os.getenv("EXTRA_IMG", "https://files.catbox.moe/uufiry.jpg")
