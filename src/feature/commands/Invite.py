from discord import Message, Embed

from feature.commands.Command import Command
from util.constants import COMMAND_IDENTIFIER, COLOR, NAME
from util.util import get_language


class Invite(Command):
    head: str = 'invite'
    emoji: str = ':postbox:'
    description_path: str = 'command.invite.description'
    usage_paths: tuple = (
        (f'{COMMAND_IDENTIFIER}{head}', 'command.invite.description'),
    )
    admin_only: bool = False

    def __init__(self, tobcidnock):
        super().__init__()

        self.tobcidnock = tobcidnock

    async def operate(self, message: Message):
        invite_language = get_language(self.tobcidnock, message.author)['command']['invite']

        embed = Embed(
            title=invite_language['description'],
            colour=COLOR
        )
        embed.add_field(
            name=invite_language['operate']['invite_link'],
            value=invite_language['operate']['click_here']
        )

        await message.channel.send(self.emoji, embed=embed)
