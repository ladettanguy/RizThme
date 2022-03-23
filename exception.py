import discord


class DuplicateGuildPlayerThreadError(Exception):
    def __init__(self, guild: discord.Guild):
        self.guild = guild

    def __str__(self):
        return f"You try to create a 2nd Player for the guilde {self.guild}"
