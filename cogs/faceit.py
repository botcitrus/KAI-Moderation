import discord
from discord import app_commands
import asyncio
from discord.ext import commands
import json
import asyncio
import random
import re
import time
from pymongo import MongoClient
import psutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import requests
import traceback
from asyncio import sleep
from io import BytesIO
import typing
import os
 
su_color=0x2ecc71
err_color=0xe74c3c
dark_red = 0x99aab5
base_color=0x8A2BE2
null_color=discord.Color.from_rgb(47,49,56)

class Faceit(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://Setroom:CFLrxCSX0fzBIMlA@cluster0.l9fw9.mongodb.net/ecodb?retryWrites=true&w=majority")
        self.colluser = self.cluster.faceit.user
        self.collgame = self.cluster.faceit.game
	
    @commands.Cog.listener()
    async def on_ready(self):
        print("Faceit cog loaded.")
	
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def game(self, ctx, name1: str = None, tag1: str = None, name2: str = None, tag2: str = None):
        tru = discord.utils.get(self.client.emojis, name='yes')
        err = discord.utils.get(self.client.emojis, name='no')
        if name1 is None:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите название первой команды!",
                color = discord.Color.red()
	    )
            await ctx.send(embed = embed)
        elif tag1 is None:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите тег первой команды!",
                color = discord.Color.red()
	    )
            await ctx.send(embed = embed)
        elif name2 is None:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите название второй команды!",
                color = discord.Color.red()
	    )
            await ctx.send(embed = embed)
        elif tag2 is None:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите тег второй команды!",
                color = discord.Color.red()
	    )
            await ctx.send(embed = embed)
        else:
            code = random.randrange(10000)
            post = {
                "code": code,
                "owner_id": ctx.author.id,
                "guild_id": ctx.guild.id,
                f"{tag1}name": name1,
                f"{tag2}name": name2,
                f"{tag1}tag": tag1,
                f"{tag2}tag": tag2,
                f"members{tag1}": [],
                f"members{tag2}": [],
                "stop": 0
            }

            self.collgame.insert_one(post)
            embed = discord.Embed(
                title = f"{tru} Успешно:",
                description = f"**{name1}** vs **{name2}**\n\nТеги команд: {tag1} vs {tag2}\n\nКод игры: {code}",
                color = 0x00FFFF
	    )
            await ctx.send(embed = embed)
		
    @commands.command()
    async def find(self, ctx, code: int = None, tag1: str = None, tag2: str = None):
        tru = discord.utils.get(self.client.emojis, name='yes')
        err = discord.utils.get(self.client.emojis, name='no')
        if code is None:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите код игры!",
                color = discord.Color.red()
	    )
            await ctx.send(embed = embed)
        elif not self.collgame.find_one({'guild_id': ctx.guild.id, "code": code}):
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Указаный вами код игры не найден!",
                color = discord.Color.red()
	    )
            await ctx.send(embed = embed)
        elif tag1 is None:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите тег первой команды!",
                color = discord.Color.red()
	    )
            await ctx.send(embed = embed)
        elif tag2 is None:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите тег второй команды!",
                color = discord.Color.red()
	    )
            await ctx.send(embed = embed)
        else:
            name1 = self.collgame.find_one({'guild_id': ctx.guild.id, "code": code})[f"{tag1}name"]
            name2 = self.collgame.find_one({'guild_id': ctx.guild.id, "code": code})[f"{tag2}name"]
            tag1 = self.collgame.find_one({'guild_id': ctx.guild.id, "code": code})[f"{tag1}tag"]
            tag2 = self.collgame.find_one({'guild_id': ctx.guild.id, "code": code})[f"{tag2}tag"]
            members1 = len(self.collgame.find_one({'guild_id': ctx.guild.id, "code": code})[f"members{tag1}"])
            members2 = len(self.collgame.find_one({'guild_id': ctx.guild.id, "code": code})[f"members{tag2}"])
            embed = discord.Embed(
                title = f"{name1} vs {name2}",
                description = f"Теги команд: {tag1}, {tag2}\n\nЗа команду {name1}: {members1}\n\nЗа команду {name2}: {members2}",
                color = 0x00FFFF
	    )
            await ctx.send(embed = embed)
		
    @commands.command()
    async def profile(self, ctx, member: discord.User = None):
        legueprof = "default"
	
        if member == None:
            member = ctx.author
	
        if not self.colluser.count_documents({"guild_id": ctx.guild.id, "user_id": member.id}):
            post = {
                "user_id": member.id,
                "guild_id": ctx.guild.id,
                "points": 50,
                "leaguepoints": legueprof
            }
            self.colluser.insert_one(post)
		
        points = self.colluser.find_one({'guild_id': ctx.guild.id, "user_id": member.id})["points"]
        league = self.colluser.find_one({'guild_id': ctx.guild.id, "user_id": member.id})["leaguepoints"]
        embed = discord.Embed(
            title = f"Профиль: {member}",
            description = f"Имя: {member.name}\nID: {member.id}\nPoints: {points}\nLeague: {league}",
            color = 0x00FFFF
        )
        await ctx.send(embed = embed)
        
    @commands.command()
    async def stavka(self, ctx, code: int = None, tag: str = None, stavka: int = None):
        tru = discord.utils.get(self.client.emojis, name='yes')
        err = discord.utils.get(self.client.emojis, name='no')
        if code is None:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите код игры!",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
        elif not self.collgame.find_one({'guild_id': ctx.guild.id, "code": code}):
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Указанный вами код не найден!",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
        elif tag is None:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите тег команды на корторую хотите поставить ставку!",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
        elif stavka is None:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите ставку!",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
        elif stavka <= 0:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите ставку больше 0!",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
        elif self.colluser.find_one({'guild_id': ctx.guild.id, "user_id": ctx.author.id})["points"] < stavka:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"На вашем балансе не достаточно points",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
        elif ctx.author.id in self.collgame.find_one({'guild_id': ctx.guild.id, "code": code})[f"members{tag}"]:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Вы уже поставили ставку на эту команду!",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
        elif self.collgame.find_one({'guild_id': ctx.guild.id, "code": code})[f"stop"] <= 1:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"К сожалению принятие ставок на эту игру остановлено, ожидаем вас на следующей игре!",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
        else:
            name = self.collgame.find_one({'guild_id': ctx.guild.id, "code": code})[f"{tag}name"]
            stavkar = self.colluser.find_one({'guild_id': ctx.guild.id, "user_id": ctx.author.id})["points"] - stavka
            self.colluser.update_one({'guild_id': ctx.guild.id, 'user_id': ctx.author.id}, {'$set':{'points': stavkar}})
            addmembers = self.collgame.find_one({'guild_id': ctx.guild.id, "code": code})[f"members{tag}"]
            addmembers.append(ctx.author.id)
            self.collgame.update_one({'guild_id': ctx.guild.id, 'code': code}, {'$set':{f'members{tag}': addmembers}})
            embed = discord.Embed(
                title = f"{tru} Успешно:",
                description = f"Вы успешно поставили ставку на {name}",
                color = 0x00FFFF
            )
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def give(self, ctx, member: discord.User = None, points: int = None):
        tru = discord.utils.get(self.client.emojis, name='yes')
        err = discord.utils.get(self.client.emojis, name='no')
        if member is None:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите пользователя которому хотите выдать points!",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
        elif points is None:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите points!",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
        elif points <= 0:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите points больше 0!",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
        else:
            point = self.colluser.find_one({'guild_id': ctx.guild.id, "user_id": member.id})["points"] + points
            self.colluser.update_one({'guild_id': ctx.guild.id, 'user_id': member.id}, {'$set':{'points': point}})
            embed = discord.Embed(
                title = f"{tru} Успешно:",
                description = f"Вы успешно выдали {points} пользователю, {member}",
                color = 0x00FFFF
            )
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def stop(self, ctx, code: int = None, stop: int = None):
        tru = discord.utils.get(self.client.emojis, name='yes')
        err = discord.utils.get(self.client.emojis, name='no')
        if code is None:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите код игры!",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
        else:
            stoper = self.collgame.find_one({'guild_id': ctx.guild.id, "code": code})["stop"] + stop
            self.collgame.update_one({'guild_id': ctx.guild.id, 'code': code}, {'$set':{'stop': stoper}})
            embed = discord.Embed(
                title = f"{tru} Успешно:",
                description = f"Вы завершили регистрацию на игру!",
                color = 0x00FFFF
            )
            await ctx.send(embed = embed)
		
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def remove(self, ctx, member: discord.User = None, points: int = None):
        tru = discord.utils.get(self.client.emojis, name='yes')
        err = discord.utils.get(self.client.emojis, name='no')
        if member is None:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите пользователя которому хотите отменить points!",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
        elif points is None:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите points!",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
        elif points <= 0:
            embed = discord.Embed(
                title = f"{err} Ошибка:",
                description = f"Укажите points больше 0!",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
        else:
            point = self.colluser.find_one({'guild_id': ctx.guild.id, "user_id": member.id})["points"] - points
            self.colluser.update_one({'guild_id': ctx.guild.id, 'user_id': member.id}, {'$set':{'points': point}})
            embed = discord.Embed(
                title = f"{tru} Успешно:",
                description = f"Вы успешно отменили {points} у пользователя, {member}",
                color = 0x00FFFF
            )
            await ctx.send(embed = embed)
		
        
async def setup(client):
    await client.add_cog(Faceit(client))
