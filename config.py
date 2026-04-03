import os
from dotenv import load_dotenv

# Load variables from .env file if it exists
if os.path.exists(".env"):
    load_dotenv(".env")

# ------------------------------ REQUIRED ------------------------------ #

# Get these from https://my.telegram.org
API_ID = int(os.getenv("API_ID", "27433131"))
API_HASH = os.getenv("API_HASH", "7f8d967471ccadf83df1f199769b43e7")

# The Main Bot Token that handles /login and /logout buttons
BOT_TOKEN = os.getenv("BOT_TOKEN", "6513440724:AAHPn5TU4o6z5i5q5EtXpY79vv5aO7e951M")

# Your Telegram User ID (The primary controller)
OWNER_ID = int(os.getenv("OWNER_ID", "6796109071"))

# ------------------------------ DATABASE ------------------------------ #

# This is essential for a hosting bot to store multiple user sessions.
# Defaulting to a local SQLite database for easy setup.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///smoker_sessions.db")

# ------------------------------ SETTINGS ------------------------------ #

# Command handler prefix for your userbots (e.g., .raid or !raid)
hl = os.getenv("CMD_HNDLR", ".")

# Users authorized to use the raid/spam commands
SUDO_USERS = list(
    map(int, os.getenv("SUDO_USERS", "6796109071").split())
)

# Auto-add the Owner to the Sudo list
if OWNER_ID not in SUDO_USERS:
    SUDO_USERS.append(OWNER_ID)

# ------------------------------ ASSETS ------------------------------ #

# Image used for the help menu and welcome messages
EXTRA_IMG = os.getenv(
    "EXTRA_IMG",
    "https://files.catbox.moe/uufiry.jpg"
)

# ------------------------------ REPO INFO ------------------------------ #

UPSTREAM_REPO = os.getenv(
    "UPSTREAM_REPO",
    "https://github.com/kranpant/SMOKER-USERBOT" 
)

UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "main")
