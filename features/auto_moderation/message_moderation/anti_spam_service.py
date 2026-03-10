from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import discord
import io

from collections import defaultdict, deque
from PIL import Image

if TYPE_CHECKING:
    from database.settings_storage.settings import SettingsStorage


@dataclass
class SpamResult:
    value: bool
    messages: list[discord.Message] = field(default_factory=list)


class AntiSpamService:
    TIME_WINDOW = 30

    def __init__(self, settings: SettingsStorage):
        self.settings = settings

        self.user_message_times: dict = defaultdict(lambda: defaultdict(lambda: deque(maxlen=5)))
        self.user_attachment_times: dict = defaultdict(lambda: defaultdict(lambda: deque(maxlen=8)))

        self.content_cache: dict = defaultdict(lambda: defaultdict(lambda: deque(maxlen=5)))
        self.domain_cache: dict = defaultdict(lambda: defaultdict(lambda: deque(maxlen=5)))
        self.attachment_hash_cache: dict = defaultdict(lambda: defaultdict(lambda: deque(maxlen=5)))

    @staticmethod
    def normalize_text(text: str) -> str:
        """Lowercase, strip non-alphanumeric chars, collapse repeated characters."""
        text = text.lower()
        result = []
        prev = None
        repeat = 0

        for char in text:
            if not char.isalnum() and char != ' ':
                continue
            if char == prev:
                repeat += 1
                if repeat >= 2:
                    continue
            else:
                repeat = 0
            result.append(char)
            prev = char

        return ''.join(result)[:300]

    def _cleanup(self, guild_id: int, cache: dict, key, timestamp: float) -> None:
        """Remove expired entries from a cache deque.

        Supports both plain-timestamp deques and (timestamp, message) tuple deques.
        """
        history = cache[guild_id][key]

        while history:
            entry = history[0]
            t = entry[0] if isinstance(entry, tuple) else entry
            if timestamp - t > self.TIME_WINDOW:
                history.popleft()
            else:
                break

        if not history:
            del cache[guild_id][key]

    def check_flood(self, guild_id: int, user_id: int, timestamp: float) -> bool:
        """Return True if the user sent FLOOD_LIMIT messages within 5 seconds."""
        self._cleanup(guild_id, self.user_message_times, user_id, timestamp)

        history = self.user_message_times[guild_id][user_id]
        history.append(timestamp)

        if len(history) < 5:
            return False

        return timestamp - history[0] < 5

    def _detect_spam(
        self,
        cache: dict,
        key: int | str,
        guild_id: int,
        timestamp: float,
        message: discord.Message,
        limit: int = 3,
    ) -> SpamResult:
        """Generic detector: flags spam when the same key appears `limit` times."""
        if len(message.content) <= 4:
            return SpamResult(value=False)

        self._cleanup(guild_id, cache, key, timestamp)

        history = cache[guild_id][key]
        history.append((timestamp, message))

        known: list[discord.Message] = [msg for _, msg in history]

        if len(known) >= limit:
            return SpamResult(value=True, messages=known)

        return SpamResult(value=False)

    def check_mass_message(
        self,
        content_hash: int,
        message: discord.Message,
        timestamp: float,
    ) -> SpamResult:
        """Detect the same message content being sent repeatedly."""
        return self._detect_spam(
            cache=self.content_cache,
            key=content_hash,
            guild_id=message.guild.id,
            timestamp=timestamp,
            message=message,
        )

    def check_link_spam(self, message: discord.Message, timestamp: float) -> SpamResult:
        """Detect repeated links from the same domain. Checks all links in the message."""
        if 'http' not in message.content:
            return SpamResult(value=False)

        results: list[SpamResult] = []

        for part in message.content.split():
            if 'http' not in part:
                continue

            try:
                domain = part.split('/')[2].lower()
            except IndexError:
                continue

            result = self._detect_spam(
                cache=self.domain_cache,
                key=domain,
                guild_id=message.guild.id,
                timestamp=timestamp,
                message=message,
            )
            if result.value:
                results.append(result)

        if results:
            merged = {id(message): message for item in results for message in item.messages}
            return SpamResult(value=True, messages=list(merged.values()))

        return SpamResult(value=False)

    async def check_attachment_spam(
        self, message: discord.Message, timestamp: float
    ) -> SpamResult:
        """Detect visually similar images sent in quick succession."""
        if not message.attachments:
            return SpamResult(value=False)

        guild_id = message.guild.id
        self._cleanup(guild_id, self.user_attachment_times, message.author.id, timestamp)

        history = self.user_attachment_times[guild_id][message.author.id]
        history.append(timestamp)

        for attachment in message.attachments:
            if attachment.size > 2_000_000:
                continue
            if not attachment.content_type.startswith('image'):
                continue
            if not any(attachment.filename.lower().endswith(ext) for ext in ('png', 'jpg', 'jpeg', 'webp')):
                continue

            img_hash = await self.image_dhash(attachment)

            for old_hash in list(self.attachment_hash_cache[guild_id].keys()):
                if self.is_similar(img_hash, old_hash) and timestamp - history[0] < 60:
                    messages = []

                    for msgs in self.attachment_hash_cache[guild_id].values():
                        for _, msg in msgs:
                            messages.append(msg)

                    if not any(m is message for m in messages):
                        messages.append(message)

                    return SpamResult(value=True, messages=messages)

            self._cleanup(guild_id, self.attachment_hash_cache, img_hash, timestamp)
            self.attachment_hash_cache[guild_id][img_hash].append((timestamp, message))

        return SpamResult(value=False)

    @staticmethod
    async def image_dhash(attachment: discord.Attachment) -> int:
        """Compute a 64-bit perceptual dHash for a Discord image attachment."""
        data = await attachment.read()
        image = Image.open(io.BytesIO(data)).convert('L').resize((9, 8))
        pixels = list(iter(image.getdata()))

        hash_value = 0
        for row in range(8):
            for col in range(8):
                hash_value <<= 1
                if pixels[row * 9 + col] > pixels[row * 9 + col + 1]:
                    hash_value |= 1

        return hash_value

    @staticmethod
    def is_similar(hash1: int, hash2: int, threshold: int = 5) -> bool:
        return (hash1 ^ hash2).bit_count() <= threshold
