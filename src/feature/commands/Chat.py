from discord import Message

from feature.commands.Command import Command
from util.constants import COMMAND_IDENTIFIER, WORK_END_EMOJI, ENGLISH_LAN
from util.util import get_language


class Chat(Command):
    head: str = 'chat'
    emoji: str = ':e_mail:'
    description_path: str = 'command.chat.description'
    usage_paths: tuple = (
        (f'{COMMAND_IDENTIFIER}{head} #<ID> <message>', 'command.chat.usage.channel'),
        (f'{COMMAND_IDENTIFIER}{head} @<ID> <message>', 'command.chat.usage.user')
    )
    admin_only: bool = True

    def __init__(self, tobcidnock):
        super().__init__()

        self.tobcidnock = tobcidnock

    async def operate(self, message: Message):
        identification, content = (self.remove_head(message.content).split(' ', 1) + [''])[:2]

        if identification.startswith('#'):
            channel = self.tobcidnock.get_channel(int(identification[1:]))
            if channel:
                await channel.send('{} {}\n> {} {}'.format(
                    self.emoji, ENGLISH_LAN['command']['chat']['operate']['message_from_dev'], content, WORK_END_EMOJI
                ))
            else:
                await message.channel.send('{} {} {}'.format(
                    self.emoji, get_language(self.tobcidnock, message.author)['command']['chat']['operate'][
                        'no_channel'],
                    WORK_END_EMOJI
                ))
        else:
            user = self.tobcidnock.get_user(int(identification[1:]))
            if user:
                await user.send('{} {}\n> {} {}'.format(
                    self.emoji, get_language(self.tobcidnock, user)['command']['chat']['operate']['message_from_dev'],
                    content, WORK_END_EMOJI
                ))
            else:
                await message.channel.send('{} {} {}'.format(
                    self.emoji, get_language(self.tobcidnock, message.author)['command']['chat']['no_user'],
                    WORK_END_EMOJI
                ))
