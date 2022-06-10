import asyncio
from typing import List, Callable, Optional

import discord


class Client(discord.Client):

    def __init__(self):
        super().__init__(loop=asyncio.get_event_loop())
        self.PREFIX = '!'
        self.commands = {}

    def add_command(self, alias: List[str], command: Callable):
        """
        add a function to all aliases.

        This function is call when a message started with the alias is sent on a discord textual channel
        :param alias: List[str], list of command, callable with a discord.Message (Without PREFIX)
        :param command: Callable, function to call when the alias is sent in a message.
        """
        for name in alias:
            if name in self.commands:
                raise ValueError(f"Command {name} already exists")
            self.commands[name] = command

    def is_valid_id(self, discord_id: int):
        user = self.get_user(discord_id)
        return user is not None

    def get_user_avatar(self, discord_id: int) -> Optional[bytes]:
        if not self.is_valid_id(discord_id):
            return None
        else:
            user: discord.User = self.get_user(discord_id)
            avatar = user.avatar_url.read()
            future = asyncio.run_coroutine_threadsafe(avatar, self.loop)
            image = future.result(timeout=3000)
            return image
