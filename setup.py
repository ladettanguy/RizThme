from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
readme = (this_directory / "README.md").read_text()


setup(
    name='rizthme',
    license='AGPL-3.0',
    author="Tanguy Ladet",
    maintainer="Tanguy Ladet",
    maintainer_email='sti2dlab.ladettanguy@gmail.com',
    author_email='sti2dlab.ladettanguy@gmail.com',
    packages=find_packages(include=['rizthme.*']),
    url='https://github.com/ladettanguy/rizthme',
    keywords=
    [
        'Discord',
        'bot',
        'bot-discord',
        "music-bot",
        "music",
        "discord.py"
    ],
    install_requires=
    [
        "discord~=1.7",
        "pytube~=12.1",
        "PyNaCl~=1.5",
        "ffmpeg==1.4",
        "multipledispatch~=0.6",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
    ],
    description="Music discord bot.",
    long_description=readme,
    long_description_content_type='text/markdown',
    zip_safe=False,
)
