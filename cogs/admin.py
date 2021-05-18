import datetime
import secrets
import time
import random

import aiohttp
import discord
from discord.ext import commands, tasks

from main import HypixelAPIKey1, PinkStats, start_time

keys = PinkStats['api_keys']


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.update_stats.start()
        self.start_time = start_time

    @commands.command()
    async def send_thing(self, ctx):
        if ctx.author.id == 324553306682818561:
            channel = self.bot.get_channel(841727592406974504)
            color = ctx.author.color
            embed = discord.Embed(title='PinkPixel Stats', colour=color, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="People using the bot:", value=f"0", inline=False)
            embed.add_field(name="Guilds the bot is in:", value=f"0", inline=False)
            embed.add_field(name="Commands the bot has:", value=f"0", inline=False)
            embed.add_field(name="Cogs the bot is using:", value=f"0", inline=False)

            await channel.send(embed=embed)

    @tasks.loop(seconds=10)
    async def update_stats(self):
        await self.bot.wait_until_ready()
        current_time = time.time()
        difference = int(round(current_time - self.start_time))
        uptime = str(datetime.timedelta(seconds=difference - 1))
        channel = self.bot.get_channel(841727592406974504)
        if self.bot.user.id == 699940714405953536:
            embed = discord.Embed(title='PinkDev Stats(inactive most of the time)',
                                  colour=discord.Colour.from_rgb(253, 185, 255),
                                  timestamp=datetime.datetime.utcnow())
            embed.add_field(name="People using the bot:", value=f"{len(self.bot.users)}", inline=False)
            embed.add_field(name="Guilds the bot is in:", value=f"{len(self.bot.guilds)}", inline=False)
            embed.add_field(name="Commands the bot has:", value=f"{len(self.bot.commands)}", inline=False)
            embed.add_field(name="Cogs the bot is using:", value=f"{len(self.bot.cogs)}", inline=False)
            embed.add_field(name="Up Time:", value=f"{uptime}", inline=False)
            message = await channel.fetch_message(841729456209002597)
            await message.edit(embed=embed)
        else:
            embed = discord.Embed(title='PinkPixel Stats',
                                  colour=discord.Colour.from_rgb(253, 185, 255),
                                  timestamp=datetime.datetime.utcnow())
            embed.add_field(name="People using the bot:", value=f"{len(self.bot.users)}", inline=False)
            embed.add_field(name="Guilds the bot is in:", value=f"{len(self.bot.guilds)}", inline=False)
            embed.add_field(name="Commands the bot has:", value=f"{len(self.bot.commands)}", inline=False)
            embed.add_field(name="Cogs the bot is using:", value=f"{len(self.bot.cogs)}", inline=False)
            embed.add_field(name="Up Time:", value=f"{uptime}", inline=False)
            channel = self.bot.get_channel(841727592406974504)
            message = await channel.fetch_message(841736890053951529)

            await message.edit(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))
