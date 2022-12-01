from setuptools import setup, find_packages


setup(
    name='rizthme',
    version='2.0.1',
    license='AGPL-3.0',
    author="Tanguy Ladet",
    author_email='sti2dlab.ladettanguy@gmail.com',
    packages=find_packages('rizthme'),
    url='https://github.com/ladettanguy/rizthme',
    keywords=['Discord', 'bot', 'bot-discord', "music-bot", "music", "discord.py"],
    install_requires=[
        "discord~=1.7.3",
        "pytube~=12.1.0",
        "PyNaCl~=1.5.0",
        "ffmpeg~=1.4",
        "multipledispatch~=0.6.0",
      ],

)
