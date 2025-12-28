import inspect
from datetime import datetime
import aiofiles
import traceback


class Logger:
    @staticmethod
    async def log(level: str, message: str, filename: str, func_info: str | None = None):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        path = f"Logs/{filename}"

        async with aiofiles.open(path, 'a', encoding='utf-8') as f:
            await f.write(
                f"[{current_time}] | {level} | {func_info or 'unknown'} | {message}\n"
            )

    async def error(self, message: str, exc: Exception | None = None):
        func_name = inspect.stack()[1].function

        if exc:
            message += "\n" + "".join(traceback.format_exception(exc))

        await self.log("ERROR", message, "system_logs.log", func_name)


    async def info(self, message: str, func_info: str):
        await self.log("INFO", message, func_info, "member_left_logs.log")

    async def bad_words(self, message: str, func_info: str):
        await self.log("INFO", message, func_info, "bad_words_logs.log")
