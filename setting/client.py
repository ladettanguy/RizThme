from typing import List, Callable

import discord


class Client(discord.Client):

    def __init__(self):
        super().__init__()
        self.PREFIX = '!'
        self.commands = {}

    def add_command(self, alias: List[str], command: Callable):
        for name in alias:
            if name in self.commands:
                raise ValueError(f"Command {name} already exists")
            self.commands[name] = command
