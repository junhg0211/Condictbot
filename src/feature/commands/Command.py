from discord import Message

from util.constants import COMMAND_IDENTIFIER


class Command:
    head: str = ''
    emoji: str = ''
    description_path: str = ''
    usage_paths: tuple = ()
    admin_only: bool = None

    def __init__(self):
        assert self.head
        assert self.emoji
        assert self.description_path
        assert self.usage_paths
        assert self.admin_only is not None

    async def operate(self, message: Message):
        pass

    def remove_head(self, content: str) -> str:
        return content[len(COMMAND_IDENTIFIER) + len(self.head) + 1:]
