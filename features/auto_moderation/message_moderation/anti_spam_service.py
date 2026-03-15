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
    SUPPORTED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'webp')

    def __init__(self, settings: SettingsStorage):
        self.settings = settings

        self.user_message_times: dict = defaultdict(lambda: defaultdict(lambda: deque(maxlen=5)))
        self.user_attachment_times: dict = defaultdict(lambda: defaultdict(lambda: deque(maxlen=8)))

        self.domain_cache: dict = defaultdict(lambda: defaultdict(lambda: deque(maxlen=5)))
        self.attachment_hash_cache: dict = defaultdict(lambda: defaultdict(lambda: deque(maxlen=5)))

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

        history = cache[guild_id][key]
        self._cleanup(
            guild_id=guild_id,
            cache=cache,
            key=key,
            timestamp=timestamp
        )
        history.append((timestamp, message))

        known: list[discord.Message] = [msg for _, msg in history]

        if len(known) >= limit:
            return SpamResult(value=True, messages=known)

        return SpamResult(value=False)

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
            merged = self._get_spam_messages(results=results)
            return SpamResult(value=True, messages=list(merged.values()))

        return SpamResult(value=False)

    async def check_attachment_spam(
            self, message: discord.Message, timestamp: float
    ) -> SpamResult:
        """Detect visually similar images sent in quick succession."""
        if not message.attachments:
            return SpamResult(value=False)

        guild_id = message.guild.id

        for attachment in message.attachments:
            if not self._is_valid_image(attachment):
                continue

            img_hash = await self.image_dhash(attachment)

            self._cleanup(
                guild_id=guild_id,
                cache=self.attachment_hash_cache,
                key=img_hash,
                timestamp=timestamp
            )

            history = self.attachment_hash_cache[guild_id][img_hash]

            history.append((timestamp, message))

            if self._is_spam_image(img_hash, guild_id, timestamp):
                messages = self._get_messages(guild_id, img_hash)
                return SpamResult(value=True, messages=messages)

        return SpamResult(value=False)

    def _is_valid_image(self, attachment: discord.Attachment) -> bool:
        return (
            attachment.size <= 2_000_000
            and attachment.content_type.startswith('image')
            and attachment.filename.lower().endswith(self.SUPPORTED_EXTENSIONS)
        )

    def _is_spam_image(
            self,
            img_hash: int,
            guild_id: int,
            timestamp: float
    ) -> bool:

        history = self.attachment_hash_cache[guild_id][img_hash]

        recent = [
            (time, message) for time, message in history
            if timestamp - time < 60
        ]

        return len(recent) >= 3

    def _get_messages(
            self,
            guild_id: int,
            img_hash: int
    ) -> list[discord.Message]:

        history = self.attachment_hash_cache[guild_id][img_hash]

        return [msg for _, msg in history]

    @staticmethod
    def _get_spam_messages(results: list[SpamResult]) -> dict[int, discord.Message]:
        result: dict[int, discord.Message] = {}
        for item in results:
            for message in item.messages:
                result[message.id] = message

        return result

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

    @staticmethod
    def _cleanup(guild_id: int, cache: dict, key: str | int, timestamp: float) -> None:
        """Removes expired entries from a cache deque.

        Supports both plain-timestamp deques and (timestamp, message) tuple deques.
        """
        history = cache[guild_id][key]

        while history:
            entry = history[0]
            t = entry[0] if isinstance(entry, tuple) else entry
            if timestamp - t > 60:
                history.popleft()
            else:
                break

        if not history:
            del cache[guild_id][key]

    def clear_user(self, guild_id: int, user_id: int) -> None:
        """Remove all cached spam data for a specific user."""

        self.user_message_times[guild_id].pop(user_id, None)

        self.user_attachment_times[guild_id].pop(user_id, None)

        for img_hash in list(self.attachment_hash_cache[guild_id].keys()):
            items = self.attachment_hash_cache[guild_id][img_hash]

            filtered = [(time, message) for time, message in items if message.author.id != user_id]

            if filtered:
                self.attachment_hash_cache[guild_id][img_hash] = filtered
            else:
                del self.attachment_hash_cache[guild_id][img_hash]
