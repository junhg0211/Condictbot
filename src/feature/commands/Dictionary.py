from asyncio import create_task
from datetime import datetime
from os import mkdir, remove, listdir
from os.path import exists, isfile, join
from pickle import dump, load
from re import findall

from discord import Message, TextChannel, Embed, User

from feature.commands.Command import Command
from feature.commands.Word import Word
from feature.request_pending_messages.RequestPendingMessage import RequestPendingMessage
from feature.request_pending_messages.RequestPendingMessageManager import RequestPendingMessageManager
from util.constants import COMMAND_IDENTIFIER, AGREED_EMOJI, DISAGREED_EMOJI, WORK_END_EMOJI, COLOR
from util.util import is_dm_channel, get_language


class Dictionary(Command):
    head: str = 'dict'
    emoji: str = ':book:'
    description_path: str = 'command.dictionary.description'
    usage_paths: tuple = (
        (f'{COMMAND_IDENTIFIER}{head} create `<name>`', 'command.dictionary.usage.create'),
        (f'{COMMAND_IDENTIFIER}{head} remove `<name>`', 'command.dictionary.usage.remove'),
        (f'{COMMAND_IDENTIFIER}{head} detail `<name>`', 'command.dictionary.usage.detail'),
        (f'{COMMAND_IDENTIFIER}{head} list', 'command.dictionary.usage.list')
    )
    admin_only: bool = False

    def __init__(self, request_pending_message_manager: RequestPendingMessageManager, word: Word, tobcidnock):
        super().__init__()

        self.request_pending_message_manager = request_pending_message_manager
        self.word = word
        self.tobcidnock = tobcidnock

    async def create_dictionary(self, name: str, user: User, channel: TextChannel):
        if is_dm_channel(channel):
            base_directory = f'./res/dictionary/dm/{user.id}'
        else:
            base_directory = f'./res/dictionary/{channel.guild.id}'

        if not exists(base_directory):
            mkdir(base_directory)

        now = datetime.now()

        with open(f'{base_directory}/{name}.pickle', 'wb') as file:
            dump({
                'AUTHOR': user.id,
                'CREATED': (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond)
            }, file)

        await channel.send('{} {} {}'.format(
            self.emoji,
            get_language(self.tobcidnock, user)["command"]["dictionary"]["create_dictionary"]["ok"].format(name),
            WORK_END_EMOJI))

    async def cancel_create_dictionary(self, channel: TextChannel, user: User):
        await channel.send('{} {} {}'.format(
            self.emoji,
            get_language(self.tobcidnock, user)["command"]["dictionary"]["cancel_create_dictionary"]["ok"],
            WORK_END_EMOJI))

    async def remove_dictionary(self, name: str, channel: TextChannel, user: User):
        if is_dm_channel(channel):
            base_directory = f'./res/dictionary/dm/{user.id}'
        else:
            base_directory = f'./res/dictionary/{channel.guild.id}'

        remove(f'{base_directory}/{name}.pickle')

        await channel.send('{} {} {}'.format(
            self.emoji,
            get_language(self.tobcidnock, user)["command"]["dictionary"]["remove_dictionary"]["ok"].format(name),
            WORK_END_EMOJI
        ))

    async def cancel_remove_directory(self, channel: TextChannel, user: User):
        await channel.send('{} {} {}'.format(
            self.emoji,
            get_language(self.tobcidnock, user)["command"]["dictionary"]["cancel_remove_dictionary"]["ok"],
            WORK_END_EMOJI
        ))

    async def operate(self, message: Message):
        operation, arg = (self.remove_head(message.content).split(' ', 1) + [''])[:2]

        name = findall(r'[A-Za-z \d]{,50}', arg)
        if not name:
            await message.channel.send('{} {} {}'.format(
                self.emoji,
                get_language(self.tobcidnock, message.author)["command"]["dictionary"]["operate"]["name_unavailable"],
                WORK_END_EMOJI
            ))
            return
        name = name[0]
        if operation == 'create':
            if is_dm_channel(message.channel):
                is_exist = exists(f'./res/dictionary/dm/{message.author.id}/{name}.pickle')
            else:
                is_exist = exists(f'./res/dictionary/{message.guild.id}/{name}.pickle')
            if not name or is_exist:
                await message.channel.send('{} {} {}'.format(
                    self.emoji,
                    get_language(self.tobcidnock, message.author)["command"]["dictionary"]["operate"]["create"]["err"],
                    WORK_END_EMOJI
                ))
                return

            rp_message = await message.channel.send('{} {}'.format(
                self.emoji,
                get_language(self.tobcidnock, message.author)['command']['dictionary']['operate']['create'][
                    'rp_message'].format(name)
            ))

            self.request_pending_message_manager.add(
                RequestPendingMessage(rp_message, message.author,
                                      {AGREED_EMOJI: lambda: create_task(
                                          self.create_dictionary(name, message.author, message.channel)),
                                       DISAGREED_EMOJI:
                                           lambda: create_task(
                                               self.cancel_create_dictionary(message.channel, message.author))}))

        elif operation == 'remove':
            if is_dm_channel(message.channel):
                base_directory = f'./res/dictionary/dm/{message.author.id}'
            else:
                base_directory = f'./res/dictionary/{message.guild.id}'
            if not (name and exists(f'{base_directory}/{name}.pickle')):
                await message.channel.send('{} {} {}'.format(
                    self.emoji,
                    get_language(self.tobcidnock, message.author)['command']['dictionary']['operate']['remove']['err'],
                    WORK_END_EMOJI
                ))
                return

            with open(f'{base_directory}/{name}.pickle', 'rb') as file:
                dictionary = load(file)

            if dictionary['AUTHOR'] != message.author.id:
                await message.channel.send('{} {} {}'.format(
                    self.emoji,
                    get_language(self.tobcidnock, message.author)['command']['dictionary']['operate']['remove'][
                        'author_not_match'], WORK_END_EMOJI
                ))
                return

            rp_message = await message.channel.send('{} {}'.format(
                self.emoji,
                get_language(self.tobcidnock, message.author)['command']['dictionary']['operate']['remove'][
                    'rp_message'].format(name)
            ))

            self.request_pending_message_manager.add(
                RequestPendingMessage(rp_message, message.author,
                                      {AGREED_EMOJI: lambda: create_task(
                                          self.remove_dictionary(name, message.channel, message.author)),
                                       DISAGREED_EMOJI: lambda: create_task(
                                           self.cancel_remove_directory(message.channel, message.author))}))

        elif operation == 'detail':
            if is_dm_channel(message.channel):
                base_directory = f'./res/dictionary/dm/{message.author.id}'
            else:
                base_directory = f'./res/dictionary/{message.guild.id}'

            if not (name and exists(f'{base_directory}/{name}.pickle')):
                await message.channel.send('{} {} {}'.format(
                    self.emoji,
                    get_language(self.tobcidnock, message.author)['command']['dictionary']['operate']['detail']['err'],
                    WORK_END_EMOJI
                ))
                return

            with open(f'{base_directory}/{name}.pickle', 'rb') as file:
                dictionary = load(file)
            embed: Embed = Embed(
                title=get_language(self.tobcidnock, message.author)['command']['dictionary']['operate']['detail'][
                    'details_of'].format(name),
                colour=COLOR)
            embed.add_field(
                name=get_language(self.tobcidnock, message.author)['command']['dictionary']['operate']['detail'][
                    'words'],
                value=str(len(dictionary)))

            if is_dm_channel(message.channel):
                embed.add_field(
                    name=get_language(self.tobcidnock, message.author)['command']['dictionary']['operate']['detail'][
                        'author'],
                    value=str(message.author))
            else:
                embed.add_field(
                    name=get_language(self.tobcidnock, message.author)['command']['dictionary']['operate']['detail'][
                        'author'],
                    value=str(message.guild.get_member(dictionary['AUTHOR'])))
            embed.add_field(
                name=get_language(self.tobcidnock, message.author)['command']['dictionary']['operate']['detail'][
                        'created_at'],
                value=str(datetime(*dictionary['CREATED'])))

            await message.channel.send(self.emoji, embed=embed)

        elif operation == 'list':
            if is_dm_channel(message.channel):
                base_directory = f'./res/dictionary/dm/{message.author.id}'
                list_message = get_language(self.tobcidnock, message.author)['command']['dictionary']['operate'][
                    'list']['dm']
            else:
                base_directory = f'./res/dictionary/{message.guild.id}'
                list_message = get_language(self.tobcidnock, message.author)['command']['dictionary']['operate'][
                    'list']['server']

            files = [f.split('.')[0] for f in listdir(base_directory) if isfile(join(base_directory, f))]

            if files:
                files = '`' + ('`, `'.join(files)) + '`'
                await message.channel.send('{} {}\n> {} {}'.format(self.emoji, list_message, files, WORK_END_EMOJI))
            else:
                await message.channel.send('{} {} {}'.format(self.emoji, get_language(self.tobcidnock, message.author)[
                    'command']['dictionary']['operate']['list']['not_exist'], WORK_END_EMOJI))

        else:
            if operation:
                await message.channel.send('{} {} {}'.format(
                    self.emoji,
                    get_language(self.tobcidnock, message.author)['command']['dictionary'][
                        'operation_not_found'].format(operation),
                    WORK_END_EMOJI
                ))
