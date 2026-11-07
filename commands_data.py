"""
Database lệnh Jockie Music (prefix m!)
Parse và chuẩn hóa từ file lệnh gốc.
Mỗi lệnh có: command string, mô tả, và alias đa ngôn ngữ (VI/EN) để fuzzy-match.
"""

JOCKIE_COMMANDS = {
    # ===== Playback / Phát nhạc =====
    "play": {
        "cmd": "p",
        "desc": "Queue a track or playlist from a search term or url",
        "aliases": [
            "phát", "hát", "mở bài", "bật nhạc", "chơi nhạc", "play",
            "mở nhạc", "đánh bài", "đánh nhạc", "nghe bài", "nghe nhạc"
        ]
    },
    "join": {
        "cmd": "join",
        "desc": "Makes me join your voice channel",
        "aliases": ["vào", "vào room", "join vc", "vô", "connect"]
    },
    "leave": {
        "cmd": "leave",
        "desc": "Makes me leave the voice channel",
        "aliases": ["rồi", "thoát", "leave", "disconnect", "out", "rồi room"]
    },
    "radio": {
        "cmd": "radio",
        "desc": "Search and play from a radio station",
        "aliases": ["radio", "đài"]
    },
    "search": {
        "cmd": "search",
        "desc": "Search for a track to play",
        "aliases": ["tìm", "tìm kiếm", "search", "kiếm bài", "tìm bài"]
    },
    "insert": {
        "cmd": "insert",
        "desc": "Insert a track right after the one that is currently playing",
        "aliases": ["chèn", "insert", "thêm ngay sau"]
    },
    "playleave": {
        "cmd": "playleave",
        "desc": "Queue a track, after it has finished playing the bot will leave",
        "aliases": ["phát rồi rồi", "playleave", "phát xong thoát"]
    },
    "playrecent": {
        "cmd": "playrecent",
        "desc": "Queue your recently played tracks",
        "aliases": ["phát gần đây", "playrecent", "nhạc vừa nghe"]
    },
    "playselect": {
        "cmd": "playselect",
        "desc": "Select and queue a single track from a playlist by url",
        "aliases": ["playselect", "chọn phát"]
    },
    "playsingle": {
        "cmd": "playsingle",
        "desc": "Queue a single track from a playlist by url",
        "aliases": ["playsingle", "phát một bài"]
    },
    "album_search": {
        "cmd": "album search",
        "desc": "Search and queue an album",
        "aliases": ["tìm album", "album search", "phát album"]
    },
    "resume_session": {
        "cmd": "resume session",
        "desc": "Resume a previous session",
        "aliases": ["tiếp tục phiên", "resume session", "mở lại phiên"]
    },
    "autoplay_toggle": {
        "cmd": "autoplay toggle",
        "desc": "Toggle autoplay",
        "aliases": ["tự động phát", "autoplay", "autoplay toggle"]
    },
    "playlist_search": {
        "cmd": "playlist search",
        "desc": "Search and queue a playlist",
        "aliases": ["tìm playlist", "playlist search"]
    },

    # ===== Control / Điều khiển =====
    "pause": {
        "cmd": "pause",
        "desc": "Pause the current session",
        "aliases": ["tạm dừng", "pause", "dừng", "stop"]
    },
    "resume": {
        "cmd": "resume",
        "desc": "Resume playing the current track",
        "aliases": ["tiếp tục", "resume", "chơi tiếp", "đánh tiếp"]
    },
    "volume": {
        "cmd": "volume",
        "desc": "Change the volume",
        "aliases": ["âm lượng", "volume", "to nhỏ", "chỉnh âm"]
    },
    "forward": {
        "cmd": "forward",
        "desc": "Wind the track forwards",
        "aliases": ["tua tới", "forward", "tua nhanh", "tua trước"]
    },
    "wind_to": {
        "cmd": "wind to",
        "desc": "Wind to the desired position in the track",
        "aliases": ["tua đến", "wind to", "nhảy đến"]
    },
    "backward": {
        "cmd": "backward",
        "desc": "Wind the track backwards",
        "aliases": ["tua lùi", "backward", "tua ngược", "lùi"]
    },
    "end_time": {
        "cmd": "end time",
        "desc": "Set the end position of the current track",
        "aliases": ["đặt kết thúc", "end time", "kết thúc"]
    },
    "start_time": {
        "cmd": "start time",
        "desc": "Set the start position of the current track",
        "aliases": ["đặt bắt đầu", "start time", "bắt đầu"]
    },

    # ===== Index / Chuyển bài =====
    "next": {
        "cmd": "next",
        "desc": "Go to the next track in the queue",
        "aliases": ["tiếp theo", "next", "bài sau", "kéo", "kéo bài"]
    },
    "skip": {
        "cmd": "skip",
        "desc": "Skip the current track",
        "aliases": ["bỏ qua", "skip", "next bài", "bỏ bài"]
    },
    "skip_to": {
        "cmd": "skip to",
        "desc": "Skip to the desired track",
        "aliases": ["nhảy đến bài", "skip to", "chuyển đến bài"]
    },
    "previous": {
        "cmd": "previous",
        "desc": "Go to the previous track in the queue",
        "aliases": ["bài trước", "previous", "lùi bài", "back"]
    },
    "vote_skip": {
        "cmd": "vote skip",
        "desc": "Vote to skip the current track",
        "aliases": ["vote skip", "bỏ phiếu skip", "vote bỏ qua"]
    },

    # ===== Repeat / Lặp lại =====
    "rewind": {
        "cmd": "rewind",
        "desc": "Rewind the current track",
        "aliases": ["quay lại đầu", "rewind", "tua về đầu"]
    },
    "restart": {
        "cmd": "restart",
        "desc": "Restart the queue",
        "aliases": ["khởi động lại", "restart", "bắt đầu lại queue"]
    },
    "repeat_queue": {
        "cmd": "repeat queue",
        "desc": "Repeat the queue",
        "aliases": [
            "lặp lại danh sách", "lặp queue", "lặp playlist", "repeat queue",
            "lặp hàng đợi", "lặp tất cả", "lặp danh sách phát"
        ]
    },
    "repeat_current": {
        "cmd": "repeat current",
        "desc": "Repeat the current track",
        "aliases": [
            "lặp bài này", "lặp lại bài", "repeat current", "lặp hiện tại",
            "lặp một bài"
        ]
    },
    "repeat_disable": {
        "cmd": "repeat disable",
        "desc": "Disable any repeating which is currently enabled",
        "aliases": ["tắt lặp", "repeat disable", "bỏ lặp", "không lặp"]
    },

    # ===== Options / Tùy chọn =====
    "select_random": {
        "cmd": "select random",
        "desc": "Select tracks in the queue at random",
        "aliases": ["chọn ngẫu nhiên", "select random", "random"]
    },
    "shuffle_repeat": {
        "cmd": "shuffle repeat",
        "desc": "Shuffle the queue every time it repeats",
        "aliases": ["trộn khi lặp", "shuffle repeat"]
    },
    "remove_after_played": {
        "cmd": "remove after played",
        "desc": "Remove tracks after they have been played",
        "aliases": ["xóa sau khi phát", "remove after played"]
    },

    # ===== Queue Management / Quản lý hàng đợi =====
    "sort": {
        "cmd": "sort",
        "desc": "Sort the queue",
        "aliases": ["sắp xếp", "sort", "xếp hàng"]
    },
    "move": {
        "cmd": "move",
        "desc": "Move a track in the queue",
        "aliases": ["di chuyển", "move", "chuyển bài"]
    },
    "swap": {
        "cmd": "swap",
        "desc": "Swap the position of two tracks",
        "aliases": ["hoán đổi", "swap", "đổi chỗ"]
    },
    "reverse": {
        "cmd": "reverse",
        "desc": "Reverse the current queue",
        "aliases": ["đảo ngược", "reverse", "đảo queue"]
    },
    "shuffle": {
        "cmd": "shuffle",
        "desc": "Shuffle the queue",
        "aliases": ["trộn", "shuffle", "xáo trộn", "random queue"]
    },
    "reorder": {
        "cmd": "reorder",
        "desc": "Order the queue by specified option",
        "aliases": ["sắp xếp lại", "reorder"]
    },
    "mass_move": {
        "cmd": "mass move",
        "desc": "Move multiple tracks in the queue",
        "aliases": ["di chuyển nhiều", "mass move"]
    },
    "clear": {
        "cmd": "clear",
        "desc": "Remove all the tracks from the queue",
        "aliases": ["xóa hết", "clear", "dọn", "xóa queue", "xóa sạch"]
    },
    "remove": {
        "cmd": "remove",
        "desc": "Remove a track from the queue",
        "aliases": ["xóa bài", "remove", "bỏ bài", "xóa một bài"]
    },
    "mass_remove": {
        "cmd": "mass remove",
        "desc": "Remove multiple tracks from the queue",
        "aliases": ["xóa nhiều bài", "mass remove"]
    },
    "remove_last": {
        "cmd": "remove last",
        "desc": "Remove the last track in the queue",
        "aliases": ["xóa bài cuối", "remove last", "bỏ cuối"]
    },
    "remove_user": {
        "cmd": "remove user",
        "desc": "Remove all tracks requested by a user",
        "aliases": ["xóa bài user", "remove user"]
    },
    "remove_range": {
        "cmd": "remove range",
        "desc": "Remove a range of tracks from the queue",
        "aliases": ["xóa khoảng", "remove range", "xóa từ"]
    },
    "remove_absent": {
        "cmd": "remove absent",
        "desc": "Remove all tracks requested by absent users",
        "aliases": ["xóa absent", "remove absent"]
    },
    "remove_current": {
        "cmd": "remove current",
        "desc": "Remove the currently playing track from the queue",
        "aliases": ["xóa bài đang phát", "remove current"]
    },
    "remove_keyword": {
        "cmd": "remove keyword",
        "desc": "Remove all the tracks containing the specified keyword",
        "aliases": ["xóa theo từ khóa", "remove keyword"]
    },
    "remove_duplicates": {
        "cmd": "remove duplicates",
        "desc": "Remove all duplicate tracks from the queue",
        "aliases": ["xóa trùng", "remove duplicates", "xóa lặp"]
    },

    # ===== Genius / Thông tin bài hát =====
    "lyrics": {
        "cmd": "lyrics",
        "desc": "Get the lyrics of a song",
        "aliases": ["lờ i bài hát", "lyrics", "lờ i nhạc"]
    },
    "song_info": {
        "cmd": "song info",
        "desc": "Get information about a song",
        "aliases": ["thông tin bài hát", "song info", "info bài"]
    },
    "top_songs": {
        "cmd": "top songs",
        "desc": "Get the top songs",
        "aliases": ["bài hàng đầu", "top songs", "xếp hạng"]
    },
    "album_info": {
        "cmd": "album info",
        "desc": "Get information about an album",
        "aliases": ["thông tin album", "album info"]
    },
    "artist_info": {
        "cmd": "artist info",
        "desc": "Get information about an artist",
        "aliases": ["thông tin nghệ sĩ", "artist info", "ca sĩ"]
    },
    "searchlyrics": {
        "cmd": "searchlyrics",
        "desc": "Search for a song by its lyrics",
        "aliases": ["tìm theo lờ i", "searchlyrics", "tìm lờ i"]
    },

    # ===== Queue Info / Xem hàng đợi =====
    "save": {
        "cmd": "save",
        "desc": "Save a song to our private messages",
        "aliases": ["lưu", "save", "lưu bài"]
    },
    "queue": {
        "cmd": "queue",
        "desc": "Get a list of the full queue",
        "aliases": ["danh sách", "queue", "hàng đợi", "list", "ds"]
    },
    "next_up": {
        "cmd": "next up",
        "desc": "Get information about the next track",
        "aliases": ["bài kế", "next up", "bài tiếp"]
    },
    "upcoming": {
        "cmd": "upcoming",
        "desc": "Get a list of all the upcoming tracks",
        "aliases": ["sắp tới", "upcoming", "bài sắp phát"]
    },
    "requested": {
        "cmd": "requested",
        "desc": "Get all the tracks requested by a user",
        "aliases": ["bài đã yêu cầu", "requested"]
    },
    "now_playing": {
        "cmd": "now playing",
        "desc": "Get information about the currently playing track",
        "aliases": ["đang phát", "now playing", "bài hiện tại", "np"]
    },
    "recently_played": {
        "cmd": "recently played",
        "desc": "View your recently listened to tracks",
        "aliases": ["vừa nghe", "recently played", "mới phát"]
    },
    "queue_information": {
        "cmd": "queue information",
        "desc": "Get information about the queue",
        "aliases": ["thông tin queue", "queue information"]
    },
    "session_statistics": {
        "cmd": "session statistics",
        "desc": "Get statistics for the current session",
        "aliases": ["thống kê phiên", "session statistics"]
    },
    "session_information": {
        "cmd": "session information",
        "desc": "Get information about the current session",
        "aliases": ["thông tin phiên", "session information"]
    },

    # ===== Misc / Khác =====
    "ping": {
        "cmd": "ping",
        "desc": "Get my ping to Discord",
        "aliases": ["ping", "độ trễ", "lag"]
    },
    "about": {
        "cmd": "about",
        "desc": "Get some information about the bot",
        "aliases": ["about", "thông tin bot"]
    },
    "clean": {
        "cmd": "clean",
        "desc": "Deletes all command related messages",
        "aliases": ["dọn tin nhắn", "clean", "xóa lệnh"]
    },
    "help": {
        "cmd": "help",
        "desc": "Help command",
        "aliases": ["giúp", "help", "trợ giúp", "hướng dẫn"]
    },
}

# Build reverse lookup: alias -> command key
COMMAND_ALIASES = {}
for key, val in JOCKIE_COMMANDS.items():
    for alias in val["aliases"]:
        COMMAND_ALIASES[alias.lower()] = key

# Các từ khóa replay / phát lại lịch sử
REPLAY_KEYWORDS = [
    "phát lại", "replay", "đánh lại", "nghe lại", "mở lại",
    "play lại", "lập lại từ đầu", "phát lại danh sách"
]
