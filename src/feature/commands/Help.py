from discord import Message, Embed

from feature.commands.Command import Command
from feature.commands.CommandManager import CommandManager
from util.constants import COMMAND_IDENTIFIER, COLOR, WORK_END_EMOJI
from util.util import get_language


class Help(Command):
    head: str = 'help'
    emoji: str = ':question:'
    description_path: str = 'command.help.description'
    usage_paths: tuple = (
        (f'{COMMAND_IDENTIFIER}{head}', 'command.help.usage.passive'),
        (f'{COMMAND_IDENTIFIER}{head} `<command>`', 'command.help.usage.command')
    )
    admin_only: bool = False

    def __init__(self, command_manager: CommandManager, tobcidnock):
        super().__init__()

        self.command_manager = command_manager
        self.tobcidnock = tobcidnock

    async def operate(self, message: Message):
        label = self.remove_head(message.content)

        if label:
            selected = None
            for command in self.command_manager.commands:
                if command.head == label:
                    selected = command

            if selected is None:
                await message.channel.send('{} {} {}'.format(
                    self.emoji,
                    get_language(self.tobcidnock, message.author)['command']['help']['operate']['label']['not_found']
                        .format(label),
                    WORK_END_EMOJI
                ))
            else:
                embed = Embed(
                    title=f'{COMMAND_IDENTIFIER}{selected.head}',
                    description=eval("get_language(self.tobcidnock, message.author)['{}']"
                                     .format("']['".join(selected.description_path.split('.')))),
                    color=COLOR)
                for usage in selected.usage_paths:
                    embed.add_field(
                        name=usage[0],
                        value=eval("get_language(self.tobcidnock, message.author)['{}']"
                                   .format("']['".join(usage[1].split('.')))),
                        inline=False)
                await message.channel.send('{} {} {}'.format(
                    self.emoji,
                    get_language(self.tobcidnock, message.author)['command']['help']['operate']['label']['details_on']
                        .format(COMMAND_IDENTIFIER, selected.head),
                    WORK_END_EMOJI
                ), embed=embed)
        else:
            commands = []
            for command in self.command_manager.commands:
                if not command.admin_only:
                    # commands.append(f'> `{COMMAND_IDENTIFIER}{command.head}` - {command.description}')
                    commands.append('> `{}{}` - {}'.format(
                        COMMAND_IDENTIFIER, command.head,
                        eval("get_language(self.tobcidnock, message.author)['{}']".format(
                            "']['".join(command.description_path.split('.'))))))
            commands = '\n'.join(commands)

            await message.channel.send('{} {}\n{} {}'.format(
                self.emoji,
                get_language(self.tobcidnock, message.author)['command']['help']['operate']['list']['here_is'],
                commands, WORK_END_EMOJI
            ))
