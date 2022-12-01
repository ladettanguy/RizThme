import discord


class DuplicateGuildPlayerThreadError(Exception):
    def __init__(self, guild: discord.Guild):
        self.guild = guild

    def __str__(self):
        return f"You try to create a 2nd Player for the guild {self.guild}"


class BadLinkError(Exception):
    def __init__(self, link: str):
        self.link = link

    def __str__(self):
        return f"Bad link: {self.link}"
