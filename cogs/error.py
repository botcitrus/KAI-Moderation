import discord
import asyncio
from discord.ext import commands
from discord.ext.commands.core import bot_has_guild_permissions
from discord.ext.commands import has_permissions, MissingPermissions
import json
import asyncio
import random
import re
import time
import psutil
import requests
import traceback
from asyncio import sleep
from datetime import datetime
import datetime
import typing
import os


base_color=0x3498db
err_color=0xe74c3c

DiscordPermissions = {
    'view_channel': 'просматривать каналы',
    'manage_channels': 'управлять каналами',
    'manage_roles': 'управлять ролями',
    'manage_emojis_and_stickers': 'управлять эмодзи и стикерами',
    'view_audit_log': 'просматривать журнала аудита',
    'view_guild_insinghts': 'просмотр аналитики сервера',
    'manage_webhooks': 'управлять вебхуками (webhooks)',
    'manage_guild': 'управлять сервером',
    'create_instant_invite': 'создание приглашения',
    'change_nickname': 'изменить никнейм',
    'manage_nicknames': 'управлять никнеймами',
    'kick_members': 'выгонять участников',
    'ban_members': 'банить участников',
    'MissingAnyRole': 'Отсутсвие роли для использование команды',
    'send_messages': 'отправлять сообщения',
    'send_messages_in_threads': 'отправлять сообщения в ветки',
    'create_public_threads': 'создать публичные ветки',
    'create_private_threads': 'создание приватных веток',
    'embed_links': 'встраивать ссылки',
    'attach_files': 'прикреплять файлы',
    'add_reactions': 'добавлять реакции',
    'use_external_emojis': 'использовать внешние эмодзи',
    'use_external_stickers': 'использовать внешние стикеры',
    'mention_everyone': 'упоминание @everyone, @here и всех ролей',
    'manage_messages': 'управлять сообщениями',
    'manage_threads': 'управление ветками',
    'read_message_history': 'читать историю сообщений',
    'send_tts_messages': 'отправка сообщений text-to-speech',
    'use_application_commands': 'использовать команды приложения',
    'connect': 'подключаться',
    'speak': 'говорить',
    'video': 'видео',
    'use_voice_activity': 'использовать режим активации по голосу',
    'priority_speaker': 'приоритетный режим',
    'mute_members': 'отключать участникам микрофон',
    'deafen_members': 'отключать участникам звук',
    'move_members': 'перемещать участников',
    'administrator': 'администратор'
}

class Error(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        err = discord.utils.get(self.client.emojis, name='no')
        ignored = commands.CommandNotFound
        if isinstance(error, ignored):
            return
        
        elif isinstance(error, commands.MissingPermissions): #commands.errors.CommandOnCooldown
            embed = discord.Embed(
                title=f'{err} Ошибка!',
                description = f"**У тебя нет прав на команду**.\n**Права**: __{', '.join(DiscordPermissions[permissions] for permissions in error.missing_perms)}__", 
                colour=err_color,
                )
            await ctx.send(embed=embed)
            
        elif isinstance(error, commands.MemberNotFound): #commands.errors.CommandOnCooldown
            embed = discord.Embed(
                title=f'{err} Ошибка!',
                description = f"**Вы указали не существующего пользователя!**", 
                colour=err_color,
                )
            await ctx.send(embed=embed)
            
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                embed = discord.Embed(
                    title=f'{err} Ошибка!',
                    description = f"**У пользователя закрыты личные сообщения**.", 
                    colour=err_color,
                    )
                return await ctx.send(embed=embed)
            except:
                pass
            
        elif isinstance(error, commands.BotMissingPermissions): #commands.errors.CommandOnCooldown
            embed = discord.Embed(
                title=f'{err} Ошибка!',
                description = f"**У бота нет прав на команду**.\n**Права**: __{', '.join(DiscordPermissions[permissions] for permissions in error.missing_perms)}__", 
                colour=err_color,
                )
            await ctx.send(embed=embed)
            
        elif isinstance(error, commands.NotOwner): #commands.errors.CommandOnCooldown
            embed = discord.Embed(
                title=f'{err} Ошибка!',
                description = f"**Данная команда доступа только создателю бота**.", 
                colour=err_color,
                )
            await ctx.send(embed=embed)
            
        else:
            raise error

async def setup(client):
    await client.add_cog(Error(client))
