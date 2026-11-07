"""
Intent Engine — phân loại tin nhắn tự nhiên thành:
  - song / playlist: tên nhạc cần phát
  - command: lệnh Jockie Music
  - replay: yêu cầu phát lại lịch sử
  - unknown: không xác định

Dùng RapidFuzz để fuzzy-match nhanh, nhẹ, không cần API ngoài.
Phù hợp chạy trên Railway free tier.
"""

import re
from rapidfuzz import process, fuzz
from commands_data import JOCKIE_COMMANDS, COMMAND_ALIASES, REPLAY_KEYWORDS

# Tốc độ tối ưu: giới hạn số lượng candidate
FUZZ_TOP_N = 5
SCORE_THRESHOLD = 72  # Ngưỡng khớp alias (0-100)


def normalize(text: str) -> str:
    """Chuẩn hóa: lowercase, xóa dấu chấm/thừa."""
    text = text.lower().strip()
    text = re.sub(r"[.!?]+$", "", text)
    return text


def is_replay_request(text: str) -> bool:
    """Kiểm tra nếu user muốn phát lại / replay lịch sử."""
    t = text.lower()
    # Kiểm tra replay keyword đứng riêng hoặc ở đầu/cuối
    for kw in REPLAY_KEYWORDS:
        if kw in t:
            # Nếu không chứa từ "lặp" (để phân biệt với repeat queue)
            if "lặp" not in t or "lại" in t:
                return True
    return False


def detect_playlist_separator(text: str):
    """
    Phát hiện nếu text chứa nhiều bài hát ngăn cách bởi dấu phẩy / xuống dòng / gạch ngang.
    Trả về list các bài hát.
    """
    # Ưu tiên dấu phẩy, dấu xuống dòng, dấu gạch đầu dòng
    for sep in ["\n", " - ", "–", "—", ", ", ","]:
        if sep in text:
            parts = [p.strip() for p in text.split(sep) if p.strip()]
            if len(parts) > 1:
                return parts
    return None


def classify_intent(text: str):
    """
    Phân loại intent từ text thô.
    Trả về dict:
      { "type": "song" | "playlist" | "command" | "replay" | "unknown",
        ...các key phụ thuộc type }
    """
    text = normalize(text)

    if not text:
        return {"type": "unknown", "raw": text}

    # 1. Replay request (phát lại lịch sử)
    if is_replay_request(text):
        return {"type": "replay", "raw": text}

    # 2. Fuzzy match với alias lệnh Jockie
    #    Lấy candidate top N để so sánh nhanh
    all_aliases = list(COMMAND_ALIASES.keys())
    result = process.extractOne(
        text, all_aliases, scorer=fuzz.WRatio, score_cutoff=SCORE_THRESHOLD
    )

    if result:
        matched_alias, score, _ = result
        cmd_key = COMMAND_ALIASES[matched_alias]
        cmd_info = JOCKIE_COMMANDS[cmd_key]

        # Nếu score cao (> 85) hoặc text ngắn khớp chính xác → coi là command
        if score > 85 or (len(text) <= 20 and score > 78):
            return {
                "type": "command",
                "key": cmd_key,
                "cmd": cmd_info["cmd"],
                "desc": cmd_info["desc"],
                "matched_alias": matched_alias,
                "score": score,
                "raw": text,
            }

        # Nếu score trung bình (72-85), kiểm tra xem text có dấu hiệu tên nhạc không
        # (ví dụ chứa ngoặc, số, từ khóa bài hát...)
        music_indicators = [
            "official", "mv", "lyrics", "audio", "ft.", "feat", "remix",
            "cover", "version", "ost", "nhạc phim", "- ", " – ", "karaoke"
        ]
        has_music_indicator = any(ind in text for ind in music_indicators)
        if has_music_indicator and score < 88:
            # Nghiêng về tên nhạc hơn là lệnh
            pass
        else:
            return {
                "type": "command",
                "key": cmd_key,
                "cmd": cmd_info["cmd"],
                "desc": cmd_info["desc"],
                "matched_alias": matched_alias,
                "score": score,
                "raw": text,
            }

    # 3. Nếu chứa URL (YouTube, Spotify, SoundCloud...) → chắc chắn là nhạc/link
    url_pattern = re.compile(r"https?://\S+")
    if url_pattern.search(text):
        return {"type": "song", "title": text, "raw": text}

    # 4. Phát hiện playlist (nhiều bài)
    songs = detect_playlist_separator(text)
    if songs and len(songs) > 1:
        return {"type": "playlist", "songs": songs, "raw": text}

    # 5. Mặc định: coi như tên bài hát / tìm kiếm
    return {"type": "song", "title": text, "raw": text}


def explain_intent(intent: dict) -> str:
    """Trả về chuỗi giải thích intent để log/debug."""
    t = intent["type"]
    if t == "command":
        return f"[COMMAND] matched '{intent['matched_alias']}' -> m!{intent['cmd']} (score={intent.get('score', 0):.1f})"
    if t == "song":
        return f"[SONG] -> m!p {intent['title']}"
    if t == "playlist":
        return f"[PLAYLIST] {len(intent['songs'])} tracks -> m!p ..."
    if t == "replay":
        return "[REPLAY] -> phát lại lịch sử"
    return "[UNKNOWN]"
