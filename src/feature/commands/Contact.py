from discord import Message

from feature.commands.Command import Command
from util.constants import COMMAND_IDENTIFIER, WORK_END_EMOJI
from util.util import get_language


class Contact(Command):
    head: str = 'contact'
    emoji: str = ':post_office:'
    description_path: str = 'command.contact.description'
    usage_paths: tuple = ((f'{COMMAND_IDENTIFIER}{head}', 'command.contact.description'),)
    admin_only: bool = False

    def __init__(self, tobcidnock):
        super().__init__()

        self.tobcidnock = tobcidnock

    async def operate(self, message: Message):
        await message.channel.send('{} {} {}'.format(
            self.emoji, get_language(self.tobcidnock, message.author)['command']['contact']['operate']['message'],
            WORK_END_EMOJI))
