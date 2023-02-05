import discord
from discord.ext import commands
from discord import app_commands
from pymongo import MongoClient
from os import listdir as ld
from collections.abc import Sequence
import os
import time
import asyncio
import datetime
import sys
import re
import requests
import traceback
import random
import contextlib
import io
import os

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix = "=", intents = intents)

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("--------")
    await client.change_presence(activity=discord.Streaming(name=f'Букмекерская компания', url="https://www.twitch.tv/qrushcsgo"))
    
async def load():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await client.load_extension(f"cogs.{file[:-3]}")

async def bot():
    await load()
    await client.start('MTA2MzEyMTkxMTE4NzUyNTc2Mg.G01aPf.ke3u0OQxn293Cb5KTQ6-Tabpy9nwJO5CWA9jH0')
    
asyncio.run(bot())
