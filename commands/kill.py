import discord

from setting import CLIENT


async def kill(message: discord.Message):
    """
    This command is for stop the CLIENT,

    If someone wants to use this command,
    his discord user's id need to be in the hard-coded id list
    :param message: discord.Message
    """
    list_admin = [290227829558345728]
    if message.author.id in list_admin:
        await message.reply("SIR, YES SIR !")
        await CLIENT.close()
