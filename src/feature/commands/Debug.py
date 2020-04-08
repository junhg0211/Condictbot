from discord import Message

from feature.commands.Command import Command
from feature.request_pending_messages.RequestPendingMessageManager import RequestPendingMessageManager


class Debug(Command):
    head: str = 'debug'
    emoji: str = ':computer:'
    description_path: str = 'debug'
    usage_paths: tuple = (('debug', 'debug'),)
    admin_only: bool = True

    def __init__(self, request_pending_message_manager: RequestPendingMessageManager):
        super().__init__()

        self.request_pending_message_manager = request_pending_message_manager

    async def operate(self, message: Message):
        if self.remove_head(message.content) == 'Request Pending Message List':
            await message.channel.send(str(self.request_pending_message_manager.messages))
