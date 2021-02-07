import asyncio
import datetime

import aiohttp
import discord
from discord import Client
from discord.ext import commands, tasks

from main import db, HypixelAPIKey1, HypixelAPIKey2

dbd = db["OnlineTracking"]


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.look_thru_all.start()
        self.apiKey1 = True

    @commands.command(pass_context=True)
    async def stalk(self, ctx, player: str = None):
        sender_id = ctx.author.id
        if player is None:
            await ctx.send("Please enter a player name")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.slothpixel.me/api/players/{player}') as resp:
                playerAPI = await resp.json()
        if 'error' in playerAPI:
            await ctx.send("Wrong Username")
            return
        check = dbd.find_one({"user_id": f"{sender_id}", "player": f"{playerAPI['uuid']}"})
        if check:
            await ctx.send("You are already stalking that person")
            return
        if playerAPI['online']:
            channel = self.bot.get_channel(806995896298110977)
            await channel.send(f"<@{sender_id}>, {playerAPI['username']} is online")
            info = {"user_id": f"{sender_id}", "player": f"{playerAPI['uuid']}", "checked": True, "dm": False}
        if not playerAPI['online']:
            info = {"user_id": f"{sender_id}", "player": f"{playerAPI['uuid']}", "checked": False, "dm": False}
        dbd.insert_one(info)
        await ctx.send(f"You are now stalking {player}")

    @commands.command(pass_context=True)
    async def un_stalk(self, ctx, player: str = None):
        sender_id = ctx.author.id
        if player is None:
            ctx.send("Please specify who you want to stop talking")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.slothpixel.me/api/players/{player}') as resp:
                playerAPI = await resp.json()
        if 'error' in playerAPI:
            await ctx.send("Wrong Username")
            return
        dbd.delete_one({"user_id": f"{sender_id}", "player": f"{playerAPI['uuid']}"})
        await ctx.send(f"You are no longer stalking {player}")

    @commands.command(pass_context=True)
    async def dm_toggle(self, ctx, player: str = None):
        sender_id = ctx.author.id
        if player is None:
            await ctx.send("Please specify for who you want to get dmd")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.slothpixel.me/api/players/{player}') as resp:
                playerAPI = await resp.json()
        if 'error' in playerAPI:
            await ctx.send("Wrong Username")
            return
        found = dbd.find_one({"user_id": f"{sender_id}", "player": f"{playerAPI['uuid']}"})
        if found:
            if not found['dm']:
                dbd.update_one({"user_id": f"{sender_id}", "player": f"{playerAPI['uuid']}"},
                               {"$set": {"dm": True}})
                await ctx.send(f"You are now getting dmd for {player}")
            else:
                dbd.update_one({"user_id": f"{sender_id}", "player": f"{playerAPI['uuid']}"},
                               {"$set": {"dm": False}})
                await ctx.send(f"You are no longer getting dmd for {player}")
        else:
            await ctx.send(f"I couldnt fin the player by the name of {player}")

    @tasks.loop(seconds=60)
    async def look_thru_all(self):
        await self.bot.wait_until_ready()
        for document in dbd.find():
            if self.apiKey1:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                            f'https://api.hypixel.net/player?key={HypixelAPIKey1}&uuid={document["player"]}') as resp:
                        playerAPI = await resp.json()
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                            f'https://api.hypixel.net/player?key={HypixelAPIKey2}&uuid={document["player"]}') as resp:
                        playerAPI = await resp.json()
            if not playerAPI['success']:
                channel = self.bot.get_channel(806934370724216882)
                await channel.send(f"API Key Request limit reached")
                break
            if playerAPI['player']["lastLogin"] > playerAPI['player']['lastLogout']:
                if not document['checked']:
                    if not document['dm']:
                        channel = self.bot.get_channel(806934370724216882)
                        await channel.send(f"<@{document['user_id']}>, {playerAPI['player']['displayname']} is online")
                        dbd.update({"user_id": document["user_id"], "player": document['player']},
                                   {"$set": {"checked": True}})
                    else:
                        user = await self.bot.fetch_user(document['user_id'])

                        print(document['user_id'])
                        print(user)
                        await user.send(f"<@{document['user_id']}>, {playerAPI['player']['displayname']} is online")
                        dbd.update({"user_id": document["user_id"], "player": document['player']},
                                   {"$set": {"checked": True}})
            if playerAPI['player']["lastLogin"] < playerAPI['player']['lastLogout']:
                if document['checked']:
                    dbd.update({"user_id": document["user_id"], "player": document['player']},
                               {"$set": {"checked": False}})
            self.apiKey1 = not self.apiKey1

    @commands.command(pass_context=True)
    async def get_people(self, ctx):
        totalPeople = 0
        color = ctx.author.color
        embed = discord.Embed(title=f'{ctx.author} list', colour=color, timestamp=datetime.datetime.utcnow())
        for document in dbd.find():
            if document['user_id'] == f"{ctx.author.id}":
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.slothpixel.me/api/players/{document["player"]}') as resp:
                        playerAPI = await resp.json()
                if document['dm']:
                    embed.add_field(name=f"{playerAPI['username']}:", value="DM Notifications", inline=False)
                else:
                    embed.add_field(name=f"{playerAPI['username']}:", value="Pinks Server Notifications", inline=False)
                totalPeople = totalPeople + 1
        if totalPeople == 0:
            embed.add_field(name="Error", value="You currently arent watching anyone", inline=False)
        else:
            embed.add_field(name="Total People", value=f"{totalPeople}", inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def total_people(self, ctx):
        totalPeople = 0
        color = ctx.author.color
        embed = discord.Embed(title=f'{ctx.author} list', colour=color, timestamp=datetime.datetime.utcnow())
        for document in dbd.find():
            totalPeople = totalPeople + 1
        embed.add_field(name="Total People", value=f"{totalPeople}", inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
