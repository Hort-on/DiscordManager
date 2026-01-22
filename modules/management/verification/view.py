import discord.ui

from modules.management.verification.buttons import AgreeButton, DisagreeButton


class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(AgreeButton())
        self.add_item(DisagreeButton())
