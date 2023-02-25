from discord import Embed
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        bot.remove_command("help")

    @commands.hybrid_command()
    async def help(self, ctx: commands.Context):
        await ctx.send(
            embed=Embed(
                title="Help",
                description="This bot only have one purpose and that is checking if a player is eligible for the tournament or not. To check if a player is eligible for the tournament, use `c!check <player name>`.\n\n**Note:** This bot only checks if a player is eligible for the tournament and give rank informations. It doesn't check if a player is in the tournament or not.\nYou can use slash command or c!check !\nNote: This bot fetch all user information (not including unranked ones) from tetr.io when <t:1677238140:F>",
            )
        )
    @commands.hybrid_command()
    async def foss(self, ctx: commands.Context):
        await ctx.send(
            embed=Embed(
                title="Foss",
                description="This bot is open source and you can find it here: https://github.com/timelessnesses/tetrio-tournament-checker-bot"
            )
        )
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))
