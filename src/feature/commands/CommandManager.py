from asyncio import sleep

from discord import Message

from util.constants import COMMAND_IDENTIFIER
from feature.commands.Command import Command
from util.util import is_dm_channel


class CommandManager:
    def __init__(self):
        self.commands = []

    def add(self, command: Command):
        self.commands.append(command)

    async def operate(self, message: Message):
        for command in self.commands:
            await sleep(0)
            if message.content.split(' ', 1)[0] == f'{COMMAND_IDENTIFIER}{command.head}':
                if command.admin_only:
                    if not is_dm_channel(message.channel):
                        if message.author.top_role.permissions.administrator:
                            await command.operate(message)
                else:
                    await command.operate(message)
