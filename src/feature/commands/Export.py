from os import mkdir
from os.path import exists

from discord import Message, File

from feature.commands.Command import Command
from util.constants import COMMAND_IDENTIFIER, WORK_END_EMOJI
from util.util import is_dm_channel, get_language, pickle_to_json


class Export(Command):
    head: str = 'export'
    emoji: str = ':arrow_down:'
    description_path: str = 'command.export.description'
    usage_paths: tuple = ((f'{COMMAND_IDENTIFIER}{head} <dictionary name>', 'command.export.usage.dictionary_name'),)
    admin_only: bool = False

    def __init__(self, tobcidnock):
        super().__init__()

        self.tobcidnock = tobcidnock

    async def operate(self, message: Message):
        name = self.remove_head(message.content)

        if is_dm_channel(message.channel):
            base_directory = f'./res/dictionary/dm/{message.author.id}'
        else:
            base_directory = f'./res/dictionary/{message.channel.guild.id}'

        dictionary_path = f'{base_directory}/{name}.pickle'

        if not exists(base_directory) or not exists(dictionary_path):
            await message.channel.send('{} {} {}'.format(
                self.emoji,
                get_language(self.tobcidnock, message.author)['command']['export']['operate']['no_dictionary'].format(
                    name
                ),
                WORK_END_EMOJI
            ))
            return

        await message.channel.send(file=File(pickle_to_json(dictionary_path)))
