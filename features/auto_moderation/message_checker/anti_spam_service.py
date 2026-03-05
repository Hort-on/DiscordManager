import re

from collections import defaultdict, deque


class AntiSpamService:
    def __init__(self):
        self.user_message_times = defaultdict(lambda: deque(maxlen=10))
        self.content_hash_cache = defaultdict(lambda: deque(maxlen=20))
        self.link_cache = defaultdict(lambda: deque(maxlen=20))

    @staticmethod
    def normalize_text(text: str) -> str:
        symbol_map = str.maketrans({
            '0': "o",
            '1': "i",
            '3': "e",
            '4': "a",
            '5': "s",
            '7': "t"
        })

        re_clean = re.compile(r'(.)\1{2,}|[^\w\s]|[aeiou]', re.I)
        re_space = re.compile(r'\s+')

        text = text.lower().translate(symbol_map)[:300]

        text = re_clean.sub(
            lambda m: m.group(1) if m.group(1) else '',
            text
        )

        return re_space.sub(' ', text).strip()

    def check_flood(self, user_id: int, timestamp: float) -> bool:
        history = self.user_message_times[user_id]
        history.append(timestamp)

        if len(history) < 5:
            return False

        return timestamp - history[0] < 5

    def check_mass_message(self, content_hash: int, user_id: int, channel_id: int, timestamp: float) -> bool:
        history = self.content_hash_cache[content_hash]

        while history and timestamp - history[0][0] > 10:
            history.popleft()

        history.append((timestamp, user_id, channel_id))

        channels = set()

        for _, _, c in history:
            channels.add(c)
            if len(channels) >= 3:
                return True

        return False

    def check_link_spam(self, domain: str, user_id: int, channel_id: int, timestamp: float) -> bool:
        history = self.link_cache[domain]

        while history and timestamp - history[0][0] > 10:
            history.popleft()

        history.append((timestamp, user_id, channel_id))

        channels = set()

        for _, _, c in history:
            channels.add(c)
            if len(channels) >= 3:
                return True

        return False
