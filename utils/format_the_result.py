from utils.get_channel_name import get_channel_name
from utils.summary_fields import SUMMARY_FIELDS, CHANNEL_FIELDS


class FormatResult:

    @staticmethod
    def format_the_result(parent, interaction, start) -> str:
        summary = ['Configuration completed!\n' if start else 'Current configuration:\n']

        for key, label in SUMMARY_FIELDS.items():
            value = parent.config.get(key, False)
            status = '✅ Enabled' if value else '❌ Disabled'
            summary.append(f"🔹 {label}: {status}")

        for key, label in CHANNEL_FIELDS.items():
            name = get_channel_name(interaction, parent.config.get(key))
            summary.append(f"🔹 {label}: {name}")

        summary_result = "\n".join(summary)

        return summary_result
