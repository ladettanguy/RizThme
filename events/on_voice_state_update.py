import asyncio
import logging
from typing import Dict

import discord

from models.mode import MODE
from setting import CLIENT
from models import Player

timeout = 10

in_progress_shedulers: Dict[discord.VoiceChannel, asyncio.Task] = {}


@CLIENT.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    """
    This event is called when a member changes voice state.

    We try to check here, if the CLIENT is alone in the voice channel.
    If so, we try to shedule a task to set a timeout before rechecking if CLIENT is always alone in the voice channel.

    If a member join the CLIENT, that's stop the sheduler.

    :param member: Member concerning the voice state update
    :param before: VoiceState object before the change
    :param after: VoiceState object after the change
    """

    # if member don't have switched voice channel, do nothing
    if before.channel == after.channel:
        return

    # if member join the voice channel, stop the asyncio.Task
    if after.channel in in_progress_shedulers.keys():
        # cancel it
        in_progress_shedulers[after.channel].cancel()
        # delete it from the dict
        del in_progress_shedulers[after.channel]

    # get the voice client of the old voice channel member. if the member not being in the bot voice channel, do nothing
    voice_client: discord.VoiceClient = discord.utils.get(CLIENT.voice_clients, channel=before.channel)
    if voice_client is None:
        return

    # an async function to check if CLIENT always alone in the voice channel after timeout (in seconds)
    async def schedule():
        # wait for timeout seconds
        await asyncio.sleep(timeout)

        # if CLIENT is alone
        if check_alone_in_voice_channel(voice_client):
            # stop music and clear the queue
            p = Player.get(voice_client.guild)
            p.clear_queue()
            p.set_mode(MODE.NORMAL)
            # disconnect from the voice channel
            dc = voice_client.disconnect()
            # delete this schedule from @in_progress_shedulers
            del in_progress_shedulers[voice_client.channel]
            await dc
            logging.info("Disconnected from voice channel. (By alone timeout task)")

    # Check if the member is in a voice channel
    if check_alone_in_voice_channel(voice_client):
        # Create a new asyncio.Task. shedule() will wait @timeout for recheck if CLIENT is alone
        task = asyncio.ensure_future(schedule())
        # add this task to @in_progress_shedulers
        in_progress_shedulers[voice_client.channel] = task


def check_alone_in_voice_channel(voice_client: discord.VoiceClient):
    """
    Check if the member is alone in the voice channel.
    :param voice_client: VoiceClient object
    :return: True if the member is alone, False otherwise
    """
    channel: discord.VoiceChannel = voice_client.channel
    if len(channel.members) == 1:
        return True
    return False
