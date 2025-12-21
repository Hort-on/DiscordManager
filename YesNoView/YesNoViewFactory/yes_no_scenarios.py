import discord


class BaseScenario:
    async def proceed(self, interaction: discord.Interaction, **kwargs):
        raise NotImplementedError


class StartConfigScenario(BaseScenario):
    def __init__(self, parent, config_key, on_decline_callback):
        self.parent = parent
        self.config_key = config_key
        self.on_decline_callback = on_decline_callback

    async def proceed(self, interaction: discord.Interaction, **kwargs):
        value: bool = kwargs.get("value")

        if self.config_key is not None:
            self.parent.config[self.config_key] = value

        if not value and self.on_decline_callback:
            await self.on_decline_callback(interaction)
            return

        await self.parent.next_step(interaction)


class ConfirmationScenario(BaseScenario):
    ...

