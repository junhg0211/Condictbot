from datetime import datetime
from pickle import load, dump

from discord import Client, Message, DMChannel, Reaction, User

from feature.commands.Contact import Contact
from feature.commands.Help import Help
from feature.commands.Random import Random
from feature.commands.Setting import Setting
from feature.commands.Word import Word
from util.constants import BOT_TOKEN, SEARCH_IDENTIFIER, COMMAND_IDENTIFIER, DEBUG, DEVELOPER_USER_IDS
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

    def dump_settings(self):
        with open('./res/settings.pickle', 'wb') as file:
            dump(self.settings, file)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        self.command_manager.add(Uptime(self))
        self.command_manager.add(Dictionary(self.request_pending_message_manager, self.word, self))
        self.command_manager.add(self.word)
        self.command_manager.add(Help(self.command_manager, self))
        self.command_manager.add(Setting(self))
        self.command_manager.add(Contact(self))
        self.command_manager.add(Random(self))
        if DEBUG:
            print('DEBUG is enabled. Only developers can use all of the features.')

            self.command_manager.add(Debug(self.request_pending_message_manager))

        with open('./res/on.pickle', 'rb') as file:
            self.on = load(file)
        self.on += 1
        with open('./res/on.pickle', 'wb') as file:
            dump(self.on, file)

    async def on_message(self, message: Message):
        if not DEBUG or (DEBUG and message.author.id in DEVELOPER_USER_IDS):
            await self.command_manager.operate(message)

            if message.content.startswith(COMMAND_IDENTIFIER) or message.content.startswith(SEARCH_IDENTIFIER) or \
                    message.author.id == self.user.id:
                if isinstance(message.channel, DMChannel):
                    print(f'{message.created_at}\t{message.channel}\t{message.author}\t{str([message.content])[2:-2]}')
                else:
                    print(f'{message.created_at}\t{message.guild}\t#{message.channel}\t{message.author}\t'
                          f'{str([message.content])[2:-2]}')

                if message.content.startswith(SEARCH_IDENTIFIER):
                    word = message.content[len(SEARCH_IDENTIFIER):]
                    if word:
                        await self.word.meaning(word, message.author, message.channel)

    async def on_reaction_add(self, reaction: Reaction, user: User):
        self.request_pending_message_manager.on_reaction_add(reaction, user)


def main():
    client = Tobcidnock()
    client.run(BOT_TOKEN)
