from datetime import datetime

from discord import Message

from util.constants import COMMAND_IDENTIFIER, WORK_END_EMOJI
from util.util import ordered, get_language
from feature.commands.Command import Command


class Uptime(Command):
    head: str = 'uptime'
    emoji: str = ':clock:'
    description_path: str = 'command.uptime.description'
    usage_paths: tuple = ((f'{COMMAND_IDENTIFIER}{head}', description_path),)
    admin_only: bool = False

    def __init__(self, tobcidnock):
        super().__init__()

        self.tobcidnock = tobcidnock

    async def operate(self, message: Message):
        await message.channel.send('{} {} {}'.format(
            self.emoji,
            get_language(self.tobcidnock, message.author)['command']['uptime']['launch'].format(
                ordered(self.tobcidnock.on), datetime.now() - self.tobcidnock.uptime),
            WORK_END_EMOJI
        ))
