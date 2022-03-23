from typing import Optional

import discord

from models import Player
from setting import CLIENT


async def play(message: discord.Message) -> None:
    """
    Commande du client discord,
    Joue de la musique dans le salon vocal de l'utilisateur qui a écrit la commande.

    La commande permet de lire les liens YouTube et de jouer l'audio sans télécharger la vidéo.

    @play permet aussi de mettre une queue, les liens appelés alors que le bot est déjà en train de jouer un son.
    :param message: discord.Message, message envoyer par l'utilisateur voulant lancer une musique
    :return: None
    """
    guild: Optional[discord.Guild] = message.guild
    if guild is None:
        return

    # Récupère le VoiceClient du bot, s'il y en a déjà un présent dans le serveur.
    voice_client = discord.utils.get(CLIENT.voice_clients, guild=guild)
    if not voice_client:
        # Récupère le channel vocal de l'auteur du message.
        voice_channel = message.author.voice.channel
        # sinon, ce connect (en créant) au serveur avec un discord.VoiceClient
        voice_client: discord.VoiceClient = await voice_channel.connect()
        # Set the new VoiceClient to the appropriate thread
        Player.set_voice_client(guild, voice_client)

    # Récupération de l'URL présent dans le contenu du message.
    await Player.add_music(message)
