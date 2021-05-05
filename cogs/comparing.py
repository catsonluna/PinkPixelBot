import asyncio
import datetime
import io

import aiohttp
import discord
from discord.ext import commands
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


class Compare(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # change to hypixel API when i get my 3rd api key
    @commands.command(name="compare", description="Get hypixel stats")
    async def compare(self, ctx, gamemode: str = None, player1: str = None, player2: str = None):
        async with ctx.typing():
            mode = gamemode.lower()
            if mode is None:
                await ctx.send("the format is: `pp>compare game player1 player2`")
                return
            if player1 is None:
                await ctx.send("the format is: `pp>compare game player1 player2`")
                return
            if player2 is None:
                await ctx.send("the format is: `pp>compare game player1 player2`")
                return
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.slothpixel.me/api/players/{player1}') as resp:
                    player1API = await resp.json()
                async with session.get(f'https://api.slothpixel.me/api/players/{player2}') as resp:
                    player2API = await resp.json()
            if 'error' in player1API:
                await ctx.send("Wrong Player1 Username")
                return
            if 'error' in player2API:
                await ctx.send("Wrong Player2 Username")
                return
            elif mode == "overall":
                if player1API['rank'] == "MVP_PLUS_PLUS":
                    player1Rank = "MVP++"
                elif player1API['rank'] == "MVP_PLUS":
                    player1Rank = "MVP+"
                elif player1API['rank'] == "VIP_PLUS":
                    player1Rank = "VIP+"
                else:
                    player1Rank = f"{player1API['rank']}"

                if player2API['rank'] == "MVP_PLUS_PLUS":
                    player2Rank = "MVP++"
                elif player2API['rank'] == "MVP_PLUS":
                    player2Rank = "MVP+"
                elif player2API['rank'] == "VIP_PLUS":
                    player2Rank = "VIP+"
                else:
                    player2Rank = f"{player2API['rank']}"

                if player1API['online']:
                    player1OnlineStatus = "Online"
                else:
                    player1OnlineStatus = "Offline"

                if player2API['online']:
                    player2OnlineStatus = "Online"
                else:
                    player2OnlineStatus = "Offline"

                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             250)
                draw.text((0, 0), "Overall:", (255, 255, 255), font=fontbig)

                draw.text((50, 500), f"Username: {player1}", (255, 255, 255),
                          font=font)
                draw.text((1300, 500), f"Username: {player2}", (255, 255, 255),
                          font=font)

                draw.text((50, 700), f"Rank: {player1Rank}", (255, 255, 255),
                          font=font)
                draw.text((1300, 700), f"Rank: {player2Rank}", (255, 255, 255),
                          font=font)

                draw.text((50, 900), f"Level: {player1API['level']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 900), f"Level: {player2API['level']}", (255, 255, 255),
                          font=font)

                draw.text((50, 1100), f"Karma: {player1API['karma']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1100), f"Karma: {player2API['karma']}", (255, 255, 255),
                          font=font)

                draw.text((50, 1300), f"Achievement Points: {player1API['achievement_points']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1300), f"Achievement Points: {player2API['achievement_points']}", (255, 255, 255),
                          font=font)

                draw.text((50, 1500), f"Last Game: {player1API['last_game']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1500), f"Last Game: {player2API['last_game']}", (255, 255, 255),
                          font=font)

                draw.text((50, 1700), f"Online Status: {player1OnlineStatus}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1700), f"Online Status: {player2OnlineStatus}", (255, 255, 255),
                          font=font)
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            elif mode == "bedwars":
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             250)
                draw.text((0, -100), "Bedwars:", (255, 255, 255), font=fontbig)

                draw.text((50, 500), f"Username: {player1}", (255, 255, 255),
                          font=font)
                draw.text((1300, 500), f"Username: {player2}", (255, 255, 255),
                          font=font)

                draw.text((50, 700), f"Star: {player1API['stats']['BedWars']['level']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 700), f"Star: {player2API['stats']['BedWars']['level']}", (255, 255, 255),
                          font=font)

                draw.text((50, 900), f"Wins: {player1API['stats']['BedWars']['wins']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 900), f"Wins: {player2API['stats']['BedWars']['wins']}", (255, 255, 255),
                          font=font)

                draw.text((50, 1100), f"Winstreak: {player1API['stats']['BedWars']['winstreak']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1100), f"Winstreak: {player2API['stats']['BedWars']['winstreak']}", (255, 255, 255),
                          font=font)

                draw.text((50, 1300), f"FKDR: {player1API['stats']['BedWars']['final_k_d']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1300), f"FKDR: {player2API['stats']['BedWars']['final_k_d']}", (255, 255, 255),
                          font=font)

                draw.text((50, 1500), f"Final Kills: {player1API['stats']['BedWars']['final_kills']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1500), f"Final Kills: {player2API['stats']['BedWars']['final_kills']}", (255, 255, 255),
                          font=font)
                draw.text((50, 1700), f"Final Deaths: {player1API['stats']['BedWars']['final_deaths']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1700), f"Final Deaths: {player2API['stats']['BedWars']['final_deaths']}", (255, 255, 255),
                          font=font)
                draw.text((50, 1900), f"Beds Destroyed: {player1API['stats']['BedWars']['beds_broken']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1900), f"Beds Destroyed: {player2API['stats']['BedWars']['beds_broken']}", (255, 255, 255),
                          font=font)
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            elif mode == "bedwars_solo":
                fkdr1 = player1API['stats']['BedWars']['gamemodes']['solo']['final_kills'] / \
                        player1API['stats']['BedWars']['gamemodes']['solo']['final_deaths']
                fkdr2 = player2API['stats']['BedWars']['gamemodes']['solo']['final_kills'] / \
                        player2API['stats']['BedWars']['gamemodes']['solo']['final_deaths']
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             250)
                draw.text((0, -100), "Bedwars Solo:", (255, 255, 255), font=fontbig)

                draw.text((50, 500), f"Username: {player1}", (255, 255, 255),
                          font=font)
                draw.text((1300, 500), f"Username: {player2}", (255, 255, 255),
                          font=font)

                draw.text((50, 700), f"Wins: {player1API['stats']['BedWars']['gamemodes']['solo']['wins']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 700), f"Wins: {player2API['stats']['BedWars']['gamemodes']['solo']['wins']}", (255, 255, 255),
                          font=font)

                draw.text((50, 900), f"Losses: {player1API['stats']['BedWars']['gamemodes']['solo']['losses']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 900), f"Losses: {player2API['stats']['BedWars']['gamemodes']['solo']['losses']}", (255, 255, 255),
                          font=font)

                draw.text((50, 1100), f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['solo']['winstreak']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1100), f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['solo']['winstreak']}", (255, 255, 255),
                          font=font)

                draw.text((50, 1300), f"FKDR: %.2f" % fkdr1, (255, 255, 255),
                          font=font)
                draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, (255, 255, 255),
                          font=font)

                draw.text((50, 1500), f"Final Kills: {player1API['stats']['BedWars']['gamemodes']['solo']['final_kills']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1500), f"Final Kills: {player2API['stats']['BedWars']['gamemodes']['solo']['final_kills']}", (255, 255, 255),
                          font=font)
                draw.text((50, 1700), f"Final Deaths: {player1API['stats']['BedWars']['gamemodes']['solo']['final_deaths']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1700), f"Final Deaths: {player2API['stats']['BedWars']['gamemodes']['solo']['final_deaths']}", (255, 255, 255),
                          font=font)
                draw.text((50, 1900), f"Beds Destroyed: {player1API['stats']['BedWars']['gamemodes']['solo']['beds_broken']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1900), f"Beds Destroyed: {player2API['stats']['BedWars']['gamemodes']['solo']['beds_broken']}", (255, 255, 255),
                          font=font)
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            elif mode == "bedwars_doubles":
                fkdr1 = player1API['stats']['BedWars']['gamemodes']['doubles']['final_kills'] / \
                        player1API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']
                fkdr2 = player2API['stats']['BedWars']['gamemodes']['doubles']['final_kills'] / \
                        player2API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             210)
                draw.text((0, -80), "Bedwars doubles:", (255, 255, 255), font=fontbig)

                draw.text((50, 500), f"Username: {player1}", (255, 255, 255),
                          font=font)
                draw.text((1300, 500), f"Username: {player2}", (255, 255, 255),
                          font=font)

                draw.text((50, 700), f"Wins: {player1API['stats']['BedWars']['gamemodes']['doubles']['wins']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 700), f"Wins: {player2API['stats']['BedWars']['gamemodes']['doubles']['wins']}", (255, 255, 255),
                          font=font)

                draw.text((50, 900), f"Losses: {player1API['stats']['BedWars']['gamemodes']['doubles']['losses']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 900), f"Losses: {player2API['stats']['BedWars']['gamemodes']['doubles']['losses']}", (255, 255, 255),
                          font=font)

                draw.text((50, 1100), f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['doubles']['winstreak']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1100), f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['doubles']['winstreak']}", (255, 255, 255),
                          font=font)

                draw.text((50, 1300), f"FKDR: %.2f" % fkdr1, (255, 255, 255),
                          font=font)
                draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, (255, 255, 255),
                          font=font)

                draw.text((50, 1500), f"Final Kills: {player1API['stats']['BedWars']['gamemodes']['doubles']['final_kills']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1500), f"Final Kills: {player2API['stats']['BedWars']['gamemodes']['doubles']['final_kills']}", (255, 255, 255),
                          font=font)
                draw.text((50, 1700), f"Final Deaths: {player1API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1700), f"Final Deaths: {player2API['stats']['BedWars']['gamemodes']['doubles']['final_deaths']}", (255, 255, 255),
                          font=font)
                draw.text((50, 1900), f"Beds Destroyed: {player1API['stats']['BedWars']['gamemodes']['doubles']['beds_broken']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1900), f"Beds Destroyed: {player2API['stats']['BedWars']['gamemodes']['doubles']['beds_broken']}", (255, 255, 255),
                          font=font)
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            elif mode in ("bedwars_threes", "bedwars_three", "bedwars_3"):
                fkdr1 = player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills'] / \
                        player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']
                fkdr2 = player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills'] / \
                        player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             210)
                draw.text((0, -80), "Bedwars 3v3v3v3:", (255, 255, 255), font=fontbig)

                draw.text((50, 500), f"Username: {player1}", (255, 255, 255),
                          font=font)
                draw.text((1300, 500), f"Username: {player2}", (255, 255, 255),
                          font=font)

                draw.text((50, 700), f"Wins: {player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['wins']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 700), f"Wins: {player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['wins']}", (255, 255, 255),
                          font=font)

                draw.text((50, 900), f"Losses: {player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['losses']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 900), f"Losses: {player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['losses']}", (255, 255, 255),
                          font=font)

                draw.text((50, 1100), f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['winstreak']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1100), f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['winstreak']}", (255, 255, 255),
                          font=font)

                draw.text((50, 1300), f"FKDR: %.2f" % fkdr1, (255, 255, 255),
                          font=font)
                draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, (255, 255, 255),
                          font=font)

                draw.text((50, 1500), f"Final Kills: {player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1500), f"Final Kills: {player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_kills']}", (255, 255, 255),
                          font=font)
                draw.text((50, 1700), f"Final Deaths: {player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1700), f"Final Deaths: {player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['final_deaths']}", (255, 255, 255),
                          font=font)
                draw.text((50, 1900), f"Beds Destroyed: {player1API['stats']['BedWars']['gamemodes']['3v3v3v3']['beds_broken']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1900), f"Beds Destroyed: {player2API['stats']['BedWars']['gamemodes']['3v3v3v3']['beds_broken']}", (255, 255, 255),
                          font=font)
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            elif mode in ("bedwars_fours", "bedwars_four", "bedwars_4"):
                fkdr1 = player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills'] / \
                        player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']
                fkdr2 = player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills'] / \
                        player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             210)
                draw.text((0, -80), "Bedwars 4v4v4v4:", (255, 255, 255), font=fontbig)

                draw.text((50, 500), f"Username: {player1}", (255, 255, 255),
                          font=font)
                draw.text((1300, 500), f"Username: {player2}", (255, 255, 255),
                          font=font)

                draw.text((50, 700), f"Wins: {player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['wins']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 700), f"Wins: {player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['wins']}", (255, 255, 255),
                          font=font)

                draw.text((50, 900), f"Losses: {player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['losses']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 900), f"Losses: {player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['losses']}", (255, 255, 255),
                          font=font)

                draw.text((50, 1100), f"Winstreak: {player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['winstreak']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1100), f"Winstreak: {player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['winstreak']}", (255, 255, 255),
                          font=font)

                draw.text((50, 1300), f"FKDR: %.2f" % fkdr1, (255, 255, 255),
                          font=font)
                draw.text((1300, 1300), f"FKDR %.2f" % fkdr2, (255, 255, 255),
                          font=font)

                draw.text((50, 1500), f"Final Kills: {player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1500), f"Final Kills: {player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_kills']}", (255, 255, 255),
                          font=font)
                draw.text((50, 1700), f"Final Deaths: {player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1700), f"Final Deaths: {player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['final_deaths']}", (255, 255, 255),
                          font=font)
                draw.text((50, 1900), f"Beds Destroyed: {player1API['stats']['BedWars']['gamemodes']['4v4v4v4']['beds_broken']}", (255, 255, 255),
                          font=font)
                draw.text((1300, 1900), f"Beds Destroyed: {player2API['stats']['BedWars']['gamemodes']['4v4v4v4']['beds_broken']}", (255, 255, 255),
                          font=font)
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
            elif mode in ("duel", "duels"):
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          65)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             250)
                draw.text((0, -100), "Duels:", (255, 255, 255), font=fontbig)

                draw.text((50, 500), f"Username: {player1}", (255, 255, 255),
                          font=font)
                draw.text((1300, 500), f"Username: {player2}", (255, 255, 255),
                          font=font)
                if 'cosmetictitle' in player1API['stats']['Duels']['settings']['active_cosmetics']:
                    draw.text((50, 700), f"Title: {player1API['stats']['Duels']['settings']['active_cosmetics']['cosmetictitle']}",
                              (255, 255, 255),
                              font=font)
                else:
                    draw.text((50, 700), f"Title: None",
                              (255, 255, 255),
                              font=font)

                if 'cosmetictitle' in player2API['stats']['Duels']['settings']['active_cosmetics']:
                    draw.text((1300, 700), f"Title: {player2API['stats']['Duels']['settings']['active_cosmetics']['cosmetictitle']}",
                              (255, 255, 255),
                              font=font)
                else:
                    draw.text((1300, 700), f"Title: None",
                              (255, 255, 255),
                              font=font)

                draw.text((50, 900), f"Wins: {player1API['stats']['Duels']['general']['wins']}",
                          (255, 255, 255),
                          font=font)
                draw.text((1300, 900), f"Wins: {player2API['stats']['Duels']['general']['wins']}",
                          (255, 255, 255),
                          font=font)

                draw.text((50, 1100), f"Losses: {player1API['stats']['Duels']['general']['losses']}",
                          (255, 255, 255),
                          font=font)
                draw.text((1300, 1100), f"Losses: {player2API['stats']['Duels']['general']['losses']}",
                          (255, 255, 255),
                          font=font)

                draw.text((50, 1300), f"Kills: {player1API['stats']['Duels']['general']['kills']}",
                          (255, 255, 255),
                          font=font)
                draw.text((1300, 1300), f"Kills: {player2API['stats']['Duels']['general']['kills']}",
                          (255, 255, 255),
                          font=font)

                draw.text((50, 1500), f"Deaths: {player1API['stats']['Duels']['general']['deaths']}",
                          (255, 255, 255),
                          font=font)
                draw.text((1300, 1500), f"Deaths: {player2API['stats']['Duels']['general']['deaths']}",
                          (255, 255, 255),
                          font=font)

                draw.text((50, 1700), f"KDR: %.2f" % player1API['stats']['Duels']['general']['kd_ratio'],
                          (255, 255, 255),
                          font=font)
                draw.text((1300, 1700), f"KDR: %.2f" % player2API['stats']['Duels']['general']['kd_ratio'],
                          (255, 255, 255),
                          font=font)

                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
            else:
                img = Image.open("infoimgimg.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Minecraftia.ttf",
                                          80)
                fontbig = ImageFont.truetype("Minecraftia.ttf",
                                             200)
                draw.text((0, 0), "Invalid Mode", (255, 0, 0), font=fontbig)

                draw.text((0, 300), "Valid Mods:", (0, 255, 0), font=font)

                draw.text((0, 500), "Overall", (0, 255, 0), font=font)
                draw.text((0, 700), "Bedwars", (0, 255, 0), font=font)
                draw.text((0, 850), "Bedwars_solo", (0, 255, 0), font=font)
                draw.text((0, 1000), "Bedwars_doubles", (0, 255, 0), font=font)
                draw.text((0, 1150), "Bedwars_threes", (0, 255, 0), font=font)
                draw.text((0, 1300), "Bedwars_fours", (0, 255, 0), font=font)

                draw.text((0, 1500), "duels", (0, 255, 0), font=font)

                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))


def setup(bot):
    bot.add_cog(Compare(bot))
