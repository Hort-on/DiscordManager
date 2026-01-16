import discord
from discord import ui


class DropMenuView(ui.View):
    def __init__(
            self,
            options: list,
            placeholder: str,
            callback,
            timeout=60
    ):
        super().__init__(timeout=timeout)
        self._callback = callback
        self.options = options
        self.page = 0
        self.placeholder = placeholder

        self.update_view()

    def update_view(self):
        self.clear_items()

        start = self.page * 25
        end = start + 25
        current_chunk = self.options[start:end]

        select_options = []
        for item in current_chunk:
            select_options.append(item)

        select = ui.Select(placeholder=self.placeholder, options=select_options)

        async def _on_select(interaction: discord.Interaction):
            await self._callback(interaction, select.values)

        select.callback = _on_select
        self.add_item(select)

        if len(self.options) > 25:
            self.add_pagination_buttons()

    def add_pagination_buttons(self):
        prev_btn = ui.Button(label='⬅️', disabled=(self.page == 0))

        async def prev_callback(inter):
            self.page -= 1
            self.update_view()
            await inter.response.edit_message(view=self)

        prev_btn.callback = prev_callback

        max_pages = (len(self.options) - 1) // 25
        next_btn = ui.Button(label='➡️', disabled=(self.page >= max_pages))

        async def next_callback(inter):
            self.page += 1
            self.update_view()
            await inter.response.edit_message(view=self)

        next_btn.callback = next_callback

        self.add_item(prev_btn)
        self.add_item(next_btn)
