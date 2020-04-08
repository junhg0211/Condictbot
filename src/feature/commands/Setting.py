from discord import Message

from feature.commands.Command import Command
from util.constants import COMMAND_IDENTIFIER, WORK_END_EMOJI
from util.util import get_language


class Setting(Command):
    head: str = 'setting'
    emoji: str = ':gear:'
    description_path: str = 'command.setting.description'
    usage_paths: tuple = (
        (f'{COMMAND_IDENTIFIER}{head} language `<english|korean|japanese>`', 'command.setting.usage.language'),
    )
    admin_only: bool = False

    def __init__(self, tobcidnock):
        super().__init__()

        self.tobcidnock = tobcidnock

    async def operate(self, message: Message):
        operation, arg = (self.remove_head(message.content).split() + [''])[:2]

        if operation == 'language':
            if message.author.id not in self.tobcidnock.settings['USER'].keys():
                self.tobcidnock.settings['USER'][message.author.id] = {'LANGUAGE': 'ENGLISH'}

            if arg == 'english':
                self.tobcidnock.settings['USER'][message.author.id]['LANGUAGE'] = 'ENGLISH'
            elif arg == 'korean':
                self.tobcidnock.settings['USER'][message.author.id]['LANGUAGE'] = 'KOREAN'
            elif arg == 'japanese':
                self.tobcidnock.settings['USER'][message.author.id]['LANGUAGE'] = 'JAPANESE'
            else:
                await message.channel.send('{} {} {}'.format(
                    self.emoji,
                    get_language(self.tobcidnock, message.author)['command']['setting']['operation'][
                        'language_unknown'],
                    WORK_END_EMOJI
                ))
                return
            self.tobcidnock.dump_settings()
            await message.channel.send('{} {} {}'.format(
                self.emoji,
                get_language(self.tobcidnock, message.author)['command']['setting']['operation']['set_language'],
                WORK_END_EMOJI
            ))
