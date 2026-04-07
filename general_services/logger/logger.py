import inspect
import traceback
from datetime import datetime
from pathlib import Path

import aiofiles


class Logger:
    @staticmethod
    async def log(
        level: str, message: str, file_name: str, func_name: str | None = None
    ):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        path = Path("logs") / file_name
        path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(path, "a", encoding="utf-8") as f:
            await f.write(
                f"[{current_time}] | {level} | {func_name or 'unknown'} | {message}\n"
            )

    async def error(self, message: str, exc: Exception | None = None):
        try:
            func_name = inspect.stack()[1].function

            if exc:
                message += "\n" + "".join(traceback.format_exception(exc))

            await self.log(
                level="ERROR",
                message=message,
                file_name="system_logs.log",
                func_name=func_name,
            )
        except Exception:
            pass
