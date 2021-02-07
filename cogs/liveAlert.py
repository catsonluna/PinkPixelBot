import asyncio
import datetime

import aiohttp
import discord
import requests
from discord.ext import tasks, commands
from twitchAPI.twitch import Twitch

from main import TwitchID, TwitchSecret


class Live(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.LiveCheck.start()
        self.client_id = TwitchID
        self.client_secret = TwitchSecret
        self.twitch = Twitch(self.client_id, self.client_secret)
        self.twitch.authenticate_app([])
        self.TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/kraken/streams/{}"
        self.live = False
        self.API_HEADERS = {
            'Client-ID': self.client_id,
            'Accept': 'application/vnd.twitchtv.v5+json',
        }

    @tasks.loop(seconds=10)
    async def LiveCheck(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(806970916935958539)
        userid = self.twitch.get_users(logins=["pinkulu"])['data'][0]['id']
        url = self.TWITCH_STREAM_API_ENDPOINT_V5.format(userid)
        try:
            req = requests.Session().get(url, headers=self.API_HEADERS)
            jsondata = req.json()
            if 'stream' in jsondata:
                if jsondata['stream'] is not None:
                    if not self.live:
                        await channel.send(f'@everyone im live on twitch \n'
                                           f'\n'
                                           f'Stats before stream: \n'
                                           f'```py\n'
                                           f'Followers: {jsondata["stream"]["channel"]["followers"]}\n'
                                           f'All time views: {jsondata["stream"]["channel"]["views"]}\n'
                                           f'```\n'
                                           f'Come and check me out at \n{jsondata["stream"]["channel"]["url"]}')
                        self.live = True
                        await self.bot.change_presence(activity=discord.Streaming(name="Pinkulu is live",
                                                                                  url=jsondata["stream"]["channel"][
                                                                                      "url"]))
                else:
                    if self.live:
                        await channel.send('Im no longer live, thanks everyone for coming, have a good day^^')
                        await self.bot.change_presence(status=discord.Status.online,
                                                       activity=discord.Game('pp>help to get started'))
                        self.live = False
        except Exception as e:
            print("Error checking user: ", e)
            return False


def setup(bot):
    bot.add_cog(Live(bot))
