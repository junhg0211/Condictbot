from datetime import datetime
from pickle import load, dump

from discord import Client, Message, DMChannel, Reaction, User, TextChannel

from feature.commands.Contact import Contact
from feature.commands.Help import Help
from feature.commands.Invite import Invite
from feature.commands.Random import Random
from feature.commands.Setting import Setting
from feature.commands.Word import Word
from util.constants import BOT_TOKEN, SEARCH_IDENTIFIER, COMMAND_IDENTIFIER, DEBUG, DEVELOPER_USER_IDS, LOG_CHANNEL
from feature.commands.CommandManager import CommandManager
from feature.commands.Debug import Debug
from feature.commands.Dictionary import Dictionary
from feature.commands.Uptime import Uptime
from feature.request_pending_messages.RequestPendingMessageManager import RequestPendingMessageManager


class Tobcidnock(Client):
    def __init__(self, **options):
        super().__init__(**options)

        self.uptime = datetime.now()

        self.request_pending_message_manager = RequestPendingMessageManager()
        self.command_manager = CommandManager()

        self.word = Word(self)

        self.settings = {}
        with open('./res/settings.pickle', 'rb') as file:
            self.settings = load(file)
        """
        'USER'
            USER_ID
                'LANGUAGE' -> 'KOREAN'
        ...
        """

        self.on = 0

        # noinspection PyTypeChecker
        self.log_channel: TextChannel = None

    def dump_settings(self):
        with open('./res/settings.pickle', 'wb') as file:
            dump(self.settings, file)

    async def log(self, log: str):
        print(log)
        await self.log_channel.send(log)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        self.log_channel = self.get_channel(LOG_CHANNEL)

        self.command_manager.add(Uptime(self))
        self.command_manager.add(Dictionary(self.request_pending_message_manager, self.word, self))
        self.command_manager.add(self.word)
        self.command_manager.add(Help(self.command_manager, self))
        self.command_manager.add(Setting(self))
        self.command_manager.add(Contact(self))
        self.command_manager.add(Random(self))
        self.command_manager.add(Invite(self))
        if DEBUG:
            log = 'DEBUG is enabled. Only developers can use all of the features.'
            await self.log(log)

            self.command_manager.add(Debug(self.request_pending_message_manager))

        with open('./res/on.pickle', 'rb') as file:
            self.on = load(file)
        self.on += 1
        with open('./res/on.pickle', 'wb') as file:
            dump(self.on, file)

        await self.log_channel.send(f'<@&623041151993380874> {self.on}번째 작동 시작합니다. ({self.uptime})')

    async def on_message(self, message: Message):
        if (not DEBUG or (DEBUG and message.author.id in DEVELOPER_USER_IDS)) and message.channel.id != LOG_CHANNEL:
            await self.command_manager.operate(message)

            if message.content.startswith(COMMAND_IDENTIFIER) or message.content.startswith(SEARCH_IDENTIFIER) or \
                    message.author.id == self.user.id:
                if isinstance(message.channel, DMChannel):
                    log = f'T{message.created_at}\tC{message.channel}\tU{message.author}' \
                          f'\n> {str([message.content])[2:-2]}'
                else:
                    log = f'T{message.created_at}\tG{message.guild}\t#{message.channel}\tU{message.author}' \
                          f'> {str([message.content])[2:-2]}'
                await self.log(log)

                if message.content.startswith(SEARCH_IDENTIFIER):
                    word = message.content[len(SEARCH_IDENTIFIER):]
                    if word:
                        await self.word.meaning(word, message.author, message.channel)

    async def on_reaction_add(self, reaction: Reaction, user: User):
        self.request_pending_message_manager.on_reaction_add(reaction, user)


def main():
    client = Tobcidnock()
    client.run(BOT_TOKEN)
