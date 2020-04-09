from random import choice, randint

from discord import Message

from feature.commands.Command import Command
from util.constants import COMMAND_IDENTIFIER, WORK_END_EMOJI
from util.util import get_language


class Random(Command):
    head: str = 'random'
    emoji: str = ':game_die:'
    description_path: str = 'command.random.description'
    usage_paths: tuple = (
        (f'{COMMAND_IDENTIFIER}{head} <number>', 'command.random.usage.number'),
        (f'{COMMAND_IDENTIFIER}{head} <consonants> <vowels> [syllable]', 'command.random.usage.word'),
    )
    admin_only: bool = False

    def __init__(self, tobcidnock):
        super().__init__()

        self.tobcidnock = tobcidnock

    async def operate(self, message: Message):
        args = self.remove_head(message.content).split()

        if len(args) < 1:
            return

        try:
            int(args[0])
        except ValueError:
            if len(args) < 2:
                return
            else:
                syllables = 2
                if len(args) >= 3:
                    try:
                        syllables = int(args[2])
                    except ValueError:
                        pass

                consonants = args[0]
                vowels = args[1]

                result = ''
                for _ in range(syllables):
                    result += f'{choice(consonants)}{choice(vowels)}'
                    if randint(0, 1):
                        result += choice(consonants)

                await message.channel.send(f'{self.emoji} {result.lower()}, {result[0].upper()}{result[1:].lower()} '
                                           f'{result.upper()} {WORK_END_EMOJI}')
        else:
            number = int(args[0])
            if number >= 1:
                await message.channel.send(f'{self.emoji} {randint(1, number)}')
            else:
                await message.channel.send('{} {} {}'.format(
                    self.emoji,
                    get_language(self.tobcidnock, message.author)['command']['random']['operate']['number'][
                        'invalid_number'],
                    WORK_END_EMOJI
                ))
