import aiofiles
from datetime import datetime


class Logger:
    @staticmethod
    async def log(level: str, message: str, filename: str):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        path = f"Logs/{filename}"
        async with aiofiles.open(path, 'a', encoding='utf-8') as f:
            await f.write(f"[{current_time}] {level} - {message}\n")

    async def error(self, message: str):
        await self.log("ERROR", message, "system_logs.log")

    async def info(self, message: str):
        await self.log("INFO", message, "member_left_logs.log")

    async def bad_words(self, message: str):
        await self.log("INFO", message, "bad_words_logs.log")
