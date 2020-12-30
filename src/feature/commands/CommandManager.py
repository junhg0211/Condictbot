from asyncio import sleep

from discord import Message

from feature.commands.Chat import Chat
from util.constants import COMMAND_IDENTIFIER, DEVELOPER_USER_IDS
from feature.commands.Command import Command
from util.util import is_dm_channel


class CommandManager:
    def __init__(self):
        self.commands = []

    def add(self, command: Command):
        self.commands.append(command)

    def initialize(self):
        self.commands.clear()

    async def operate(self, message: Message):
        for command in self.commands:
            await sleep(0)
            if message.content.split(' ', 1)[0] == f'{COMMAND_IDENTIFIER}{command.head}':
                if isinstance(command, Chat):
                    if message.author.id in DEVELOPER_USER_IDS:
                        await command.operate(message)
                        return
                elif command.admin_only:
                    if not is_dm_channel(message.channel):
                        if message.author.top_role.permissions.administrator:
                            await command.operate(message)
                            return
                else:
                    await command.operate(message)
                    return
