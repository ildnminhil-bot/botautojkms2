"""
History Manager — lưu trữ & quản lý lịch sử bài hát đã phát.
Lưu trong memory (list) + hỗ trợ persist ra JSON nếu cần.
"""

import json
import os
from collections import deque
from typing import List

HISTORY_FILE = os.environ.get("HISTORY_FILE", "history.json")
MAX_HISTORY = int(os.environ.get("MAX_HISTORY", 500))


class HistoryManager:
    def __init__(self):
        self._queue: deque = deque(maxlen=MAX_HISTORY)
        self._load()

    def _load(self):
        """Load history từ file nếu có."""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        self._queue.append(item)
            except Exception:
                pass

    def _save(self):
        """Persist ra file JSON."""
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(list(self._queue), f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def add(self, title: str):
        """Thêm một bài vào lịch sử."""
        self._queue.append(title)
        self._save()

    def add_many(self, titles: List[str]):
        """Thêm nhiều bài."""
        for t in titles:
            self._queue.append(t)
        self._save()

    def get_all(self) -> List[str]:
        """Lấy toàn bộ lịch sử."""
        return list(self._queue)

    def get_last_n(self, n: int = 10) -> List[str]:
        """Lấy n bài gần nhất."""
        return list(self._queue)[-n:]

    def clear(self):
        """Xóa lịch sử."""
        self._queue.clear()
        self._save()

    def replay_list(self, n: int = None) -> List[str]:
        """
        Trả về danh sách cần replay.
        Nếu n=None → replay toàn bộ.
        """
        all_items = list(self._queue)
        if n is None or n >= len(all_items):
            return all_items
        return all_items[-n:]


# Singleton
def get_history() -> HistoryManager:
    if not hasattr(get_history, "_instance"):
        get_history._instance = HistoryManager()
    return get_history._instance
