from asyncio import wait, create_task

from discord import Message, User


class RequestPendingMessage:
    def __init__(self, message: Message, requester: User, requests):
        self.requests = requests
        self.requester = requester
        self.message = message

        assert len(self.requests) <= 20

        tasks = []
        for emoji in self.requests.keys():
            tasks.append(self.message.add_reaction(emoji))
        create_task(wait(tasks))

    def emojies(self):
        return self.requests.keys()

    def react(self, emoji: str):
        self.requests[emoji]()
