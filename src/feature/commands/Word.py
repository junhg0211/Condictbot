from os.path import exists
from pickle import load, dump

from discord import Message, User, TextChannel

from feature.commands.Command import Command
from util.constants import COMMAND_IDENTIFIER, WORK_END_EMOJI
from util.util import is_dm_channel, is_available_dictionary_name, tokenize, get_language


class Word(Command):
    head: str = 'word'
    emoji: str = ':crossed_swords:'
    description_path: str = 'command.word.description'
    usage_paths: tuple = (
        (f'{COMMAND_IDENTIFIER}{head} dictionary `<name>`', 'command.word.usage.select'),
        (f'{COMMAND_IDENTIFIER}{head} dictionary', 'command.word.usage.dictionary'),
        (f'{COMMAND_IDENTIFIER}{head} define `<word>` `<meaning>`', 'command.word.usage.define'),
        (f'{COMMAND_IDENTIFIER}{head} define `<word>`', 'command.word.usage.delete'),
        (f'{COMMAND_IDENTIFIER}{head} delete `<word>`', 'command.word.usage.delete'),
        (f'{COMMAND_IDENTIFIER}{head} meaning `<word>`', 'command.word.usage.meaning'),
        (f'{COMMAND_IDENTIFIER}{head} `<word>`', 'command.word.usage.meaning')
    )
    admin_only: bool = False

    def __init__(self, tobcidnock):
        super().__init__()

        self.tobcidnock = tobcidnock

        self.dictionary_selection = {'DM': {}}
        """
        SERVER_ID
            MEMBER_ID 1
                DICTIONARY_NAME
        'DM'
            MEMBER_ID
                DICTIONARY_NAME
        """

    def is_selected(self, user: User, channel: TextChannel) -> bool:
        return self.get_dictionary_name(user, channel) is not None

    def get_dictionary_name(self, user: User, channel: TextChannel):
        if is_dm_channel(channel):
            if user.id in self.dictionary_selection['DM']:
                return self.dictionary_selection['DM'][user.id]
        else:
            if channel.guild.id in self.dictionary_selection:
                if user.id in self.dictionary_selection[channel.guild.id]:
                    return self.dictionary_selection[channel.guild.id][user.id]

    def get_selected_dictionary(self, user: User, channel: TextChannel) -> dict:
        dictionary_path = self.get_dictionary_path(user, channel)

        if dictionary_path:
            with open(dictionary_path, 'rb') as file:
                return load(file)

    def dump_to_selected_dictionary(self, dictionary: dict, user: User, channel: TextChannel):
        dictionary_path = self.get_dictionary_path(user, channel)

        if dictionary_path:
            with open(dictionary_path, 'wb') as file:
                dump(dictionary, file)

    def get_dictionary_path(self, user: User, channel: TextChannel) -> str:
        dictionary_path = './res/dictionary/'
        dictionary_name = self.get_dictionary_name(user, channel)
        if dictionary_name:
            dictionary_path += (f'dm/{user.id}' if is_dm_channel(channel) else str(channel.guild.id)) + \
                               f'/{dictionary_name}.pickle'
            return dictionary_path

    async def delete_word_and_dump_and_send_message(self, word: str, dictionary: dict, user: User,
                                                    channel: TextChannel):
        if word in dictionary:
            del dictionary[word]
            self.dump_to_selected_dictionary(dictionary, user, channel)
            await channel.send('{} {} {}'.format(
                self.emoji,
                get_language(self.tobcidnock, user)['command']['word']['delete_word_and_dump_and_send_message']['ok']
                    .format(word),
                WORK_END_EMOJI
            ))
        else:
            await channel.send('{} {} {}'.format(
                self.emoji,
                get_language(self.tobcidnock, user)['command']['word']['delete_word_and_dump_and_send_message']['err']
                    .format(word),
                WORK_END_EMOJI
            ))

    async def meaning(self, arg: str, user: User, channel: TextChannel):
        dictionary = self.get_selected_dictionary(user, channel)
        dictionary_name = self.get_dictionary_name(user, channel)
        if dictionary is not None:
            exist = False
            exist_result = ''
            if arg in dictionary:
                exist = True
                exist_result = '{} {}: **__{}__**'.format(
                    self.emoji,
                    get_language(self.tobcidnock, user)['command']['word']['meaning']['word_in_language']
                        .format(arg, dictionary_name),
                    dictionary[arg])
            words = set()
            for word, meaning in dictionary.items():
                if word not in ('AUTHOR', 'CREATED'):
                    if arg.lower() in word.lower() or arg.lower() in meaning.lower():
                        words.add((word, meaning))
            result = []
            for word, meaning in words:
                result.append(f'> {word} - {meaning}')

            word_list = ''
            if result:
                word_count = len(result)
                result = '\n'.join(result[:10])

                word_list = '{}\n{}'.format(
                    get_language(self.tobcidnock, user)['command']['word']['meaning']['word_list'].format(
                        min(word_count, 10), arg),
                    result)

                if word_count > 10:
                    word_list += '\n{}'.format(
                        get_language(self.tobcidnock, user)['command']['word']['meaning'][
                            'word_list_extra'].format(word_count - 10))
            if exist:
                await channel.send(f'{exist_result}. {word_list} {WORK_END_EMOJI}')
            else:
                await channel.send('{} {} {} {}'.format(
                    self.emoji,
                    get_language(self.tobcidnock, user)['command']['word']['meaning']['not_found'].format(arg),
                    word_list, WORK_END_EMOJI
                ))
        else:
            await channel.send('{} {} {}'.format(
                self.emoji, get_language(self.tobcidnock, user)['command']['word']['dictionary_not_select'],
                WORK_END_EMOJI
            ))

    async def operate(self, message: Message):
        operation, arg = (self.remove_head(message.content).split(' ', 1) + [''])[:2]

        if operation not in ('dictionary', 'define', 'delete', 'meaning'):
            operation, arg = 'meaning', operation

        if operation == 'dictionary':
            if arg:
                if is_available_dictionary_name(arg):
                    if is_dm_channel(message.channel):
                        if exists(f'./res/dictionary/dm/{message.author.id}/{arg}.pickle'):
                            self.dictionary_selection['DM'][message.author.id] = arg
                            await message.channel.send('{} {} {}'.format(
                                self.emoji,
                                get_language(self.tobcidnock, message.author)['command']['word']['operate'][
                                    'dictionary']['ok'].format(arg),
                                WORK_END_EMOJI
                            ))
                        else:
                            await message.channel.send('{} {} {}'.format(
                                self.emoji,
                                get_language(self.tobcidnock, message.author)['command']['word']['operate'][
                                    'dictionary']['not_found'].format(arg),
                                WORK_END_EMOJI
                            ))
                    else:
                        if exists(f'./res/dictionary/{message.guild.id}/{arg}.pickle'):
                            self.dictionary_selection[message.guild.id] = {}
                            self.dictionary_selection[message.guild.id][message.author.id] = arg
                            await message.channel.send('{} {} {}'.format(
                                self.emoji,
                                get_language(self.tobcidnock, message.author)['command']['word']['operate'][
                                    'dictionary']['ok'].format(arg),
                                WORK_END_EMOJI
                            ))
                        else:
                            await message.channel.send('{} {} {}'.format(
                                self.emoji,
                                get_language(self.tobcidnock, message.author)['command']['word']['operate'][
                                    'dictionary']['not_found'].format(arg),
                                WORK_END_EMOJI
                            ))
                else:
                    await message.channel.send('{} {} {}'.format(
                        self.emoji,
                        get_language(self.tobcidnock, message.author)['command']['word']['operate']['dictionary'][
                            'unavailable'],
                        WORK_END_EMOJI
                    ))
            else:
                name = self.get_dictionary_name(message.author, message.channel)
                if name is None:
                    await message.channel.send('{} {} {}'.format(
                        self.emoji,
                        get_language(self.tobcidnock, message.author)['command']['word']['operate']['dictionary'][
                            'not_selected'].format(message.author),
                        WORK_END_EMOJI
                    ))
                else:
                    await message.channel.send('{} {} {}'.format(
                        self.emoji,
                        get_language(self.tobcidnock, message.author)['command']['word']['operate']['dictionary'][
                            'selecting'].format(message.author, name),
                        WORK_END_EMOJI
                    ))
        elif operation == 'define':
            tmp = (tokenize(arg) + [''])
            word, meaning = tmp[0], ' '.join(tmp[1:])
            word = word.lower()

            dictionary = self.get_selected_dictionary(message.author, message.channel)

            if dictionary is not None:
                if meaning:
                    dictionary[word] = meaning
                    self.dump_to_selected_dictionary(dictionary, message.author, message.channel)
                    await message.channel.send('{} {} {}'.format(
                        self.emoji,
                        get_language(self.tobcidnock, message.author)['command']['word']['operate']['define']['ok']
                            .format(word, meaning),
                        WORK_END_EMOJI
                    ))
                else:
                    await self.delete_word_and_dump_and_send_message(word, dictionary, message.author, message.channel)
            else:
                await message.channel.send('{} {} {}'.format(
                    self.emoji, get_language(self.tobcidnock, message.author)['command']['word'][
                        'dictionary_not_select'],
                    WORK_END_EMOJI
                ))

        elif operation == 'delete':
            await self.delete_word_and_dump_and_send_message(
                arg, self.get_selected_dictionary(message.author, message.channel), message.author, message.channel)

        elif operation == 'meaning':
            await self.meaning(arg, message.author, message.channel)
