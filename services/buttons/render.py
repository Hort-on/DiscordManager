from dataclasses import dataclass
from typing import Optional

import discord


@dataclass
class Render:
    content: Optional[str] = None
    embed: Optional[discord.Embed] = None
    view: Optional[discord.ui.View] = None
