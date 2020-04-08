from discord import Message, Reaction, User

from feature.request_pending_messages.RequestPendingMessage import RequestPendingMessage


class RequestPendingMessageManager:
    def __init__(self):
        self.messages = []

    def add(self, request_pending_message: RequestPendingMessage):
        self.messages.append(request_pending_message)

    def on_reaction_add(self, reaction: Reaction, user: User):
        request_pending_message = self.search_message(reaction.message)

        if request_pending_message is not None:
            if request_pending_message.requester.id == user.id:
                if reaction.emoji in request_pending_message.emojies():
                    request_pending_message.react(reaction.emoji)
                    self.messages.remove(request_pending_message)

    def search_message(self, message: Message) -> RequestPendingMessage:
        for request_pending_message in self.messages:
            if request_pending_message.message.id == message.id:
                return request_pending_message
