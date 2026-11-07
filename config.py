"""
Cấu hình bot — load từ biến môi trường (phù hợp Railway).
"""

import os
from dotenv import load_dotenv

load_dotenv()

# === BẮT BUỘC ===
OWNER_ID = int(os.environ["OWNER_ID"])          # Discord ID của bạn
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]      # User Token (self-bot) hoặc Bot Token

# === TÙY CHỌN ===
TARGET_GUILD_ID = os.environ.get("TARGET_GUILD_ID")       # Server ID (nếu muốn giới hạn)
TARGET_CHANNEL_ID = os.environ.get("TARGET_CHANNEL_ID")   # Channel ID (nếu muốn giới hạn)

JOCKIE_PREFIX = os.environ.get("JOCKIE_PREFIX", "m!")
DELAY_BETWEEN_CMDS = float(os.environ.get("DELAY_BETWEEN_CMDS", "2.5"))  # Giây
ENABLE_REPLAY_HISTORY = os.environ.get("ENABLE_REPLAY_HISTORY", "true").lower() == "true"

# Log
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
