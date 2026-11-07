"""
Jockie Music Controller Bot
- Tự động gửi lệnh m!... thay bạn qua User Account (self-bot).
- Nhận diện tên nhạc / lệnh tự nhiên bằng fuzzy-match AI.
- Lưu lịch sử, hỗ trợ replay.

⚠️ Self-bot vi phạm ToS Discord nếu lạm dụng. Chỉ dùng cho mục đích cá nhân,
   với account đã được phê duyệt và KHÔNG spam.
"""

import asyncio
import logging
import sys

import discord

import config
from intent_engine import classify_intent, explain_intent
from history_manager import get_history

# ========== Logging ==========
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("jockie-controller")

# ========== Client ==========
# discord.py-self dùng import giống discord
# Nếu bạn cài discord.py-self thì `import discord` sẽ tự động override.
class JockieController(discord.Client):
    def __init__(self):
        # intents cơ bản
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        super().__init__(intents=intents)
        self.history = get_history()

    async def on_ready(self):
        logger.info(f"✅ Đã đăng nhập: {self.user} (ID: {self.user.id})")
        logger.info(f"📦 Guilds: {[g.name for g in self.guilds]}")

    async def on_message(self, message: discord.Message):
        # Bỏ qua tin nhắn của chính mình
        if message.author.id == self.user.id:
            return

        # Chỉ phản hồi OWNER
        if message.author.id != config.OWNER_ID:
            return

        # Nếu có giới hạn channel/guild
        if config.TARGET_CHANNEL_ID and str(message.channel.id) != config.TARGET_CHANNEL_ID:
            return
        if config.TARGET_GUILD_ID and str(message.guild.id) != config.TARGET_GUILD_ID:
            return

        raw = message.content.strip()
        if not raw:
            return

        # Phân loại intent
        intent = classify_intent(raw)
        logger.info(f"📝 {message.author}: {raw!r}")
        logger.info(f"🔍 {explain_intent(intent)}")

        await self._execute_intent(message.channel, intent)

    async def _execute_intent(self, channel: discord.TextChannel, intent: dict):
        """Thực thi intent đã phân loại."""
        itype = intent["type"]

        if itype == "command":
            cmd_line = f"{config.JOCKIE_PREFIX}{intent['cmd']}"
            await channel.send(cmd_line)
            logger.info(f"➡️ Gửi: {cmd_line}")

        elif itype == "song":
            title = intent["title"]
            cmd_line = f"{config.JOCKIE_PREFIX}p {title}"
            await channel.send(cmd_line)
            self.history.add(title)
            logger.info(f"➡️ Gửi: {cmd_line}")

        elif itype == "playlist":
            songs = intent["songs"]
            for idx, song in enumerate(songs, 1):
                cmd_line = f"{config.JOCKIE_PREFIX}p {song}"
                await channel.send(cmd_line)
                self.history.add(song)
                logger.info(f"➡️ [{idx}/{len(songs)}] Gửi: {cmd_line}")
                if idx < len(songs):
                    await asyncio.sleep(config.DELAY_BETWEEN_CMDS)

        elif itype == "replay":
            await self._handle_replay(channel, intent["raw"])

        elif itype == "unknown":
            # Không hiểu → thử coi như tên nhạc cho an toàn
            title = intent.get("raw", "")
            if title:
                cmd_line = f"{config.JOCKIE_PREFIX}p {title}"
                await channel.send(cmd_line)
                self.history.add(title)
                logger.info(f"➡️ [unknown->song] Gửi: {cmd_line}")

    async def _handle_replay(self, channel: discord.TextChannel, raw_text: str):
        """
        Xử lý yêu cầu replay / phát lại.
        - Nếu text chứa số (VD: phát lại 5 bài) → replay N bài gần nhất.
        - Nếu không → replay toàn bộ lịch sử.
        """
        import re

        # Tìm số trong câu
        nums = re.findall(r"\d+", raw_text)
        n = int(nums[0]) if nums else None

        tracks = self.history.replay_list(n)
        if not tracks:
            await channel.send("📭 Lịch sử trống, không có gì để phát lại.")
            return

        limit_str = f"{n} bài gần nhất" if n else "toàn bộ lịch sử"
        logger.info(f"🔄 Replay {limit_str} ({len(tracks)} bài)")

        for idx, song in enumerate(tracks, 1):
            cmd_line = f"{config.JOCKIE_PREFIX}p {song}"
            await channel.send(cmd_line)
            logger.info(f"➡️ [REPLAY {idx}/{len(tracks)}] {cmd_line}")
            if idx < len(tracks):
                await asyncio.sleep(config.DELAY_BETWEEN_CMDS)


# ========== Startup ==========
if __name__ == "__main__":
    client = JockieController()
    try:
        client.run(config.DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"❌ Lỗi khởi động: {e}")
        sys.exit(1)
