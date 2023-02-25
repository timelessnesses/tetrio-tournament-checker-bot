import asyncpg
from discord import Color, Embed
from discord.ext import commands


class Checker(commands.Cog):
    def __init__(self, bot: commands.Bot, db: asyncpg.Connection) -> None:
        super().__init__()
        self.bot = bot
        self.db = db

    @commands.hybrid_command()
    async def check(self, ctx: commands.Context, *, user_name: str) -> None:
        info = await self.db.fetch(
            "SELECT * FROM player_history WHERE $1 LIKE '%' || name || '%'", user_name
        )
        if not info:
            await ctx.send(
                embed=Embed(
                    title="User not found",
                    description="Looks like you're not in the database. Are you unranked or newly registered account?",
                    color=Color.red(),
                )
            )
            return
        elif len(info) > 1:
            em = Embed(
                title="Multiple users found",
                description="Looks like there are multiple users with the same name. Are you in any of these?",
                color=Color.yellow(),
            )
            for i in info:
                em.add_field(
                    name=i["name"],
                    value=f"Rank: {i['rank']}\nTR: {i['tr']}\nIs Eligible for the tournament: True\nBracket: {'u' + '+' if i['rank'].lower()  in ('u','x') else 'ss' + '-'}",
                )
            await ctx.send(embed=em)
            return
        else:
            info = info[0]
            await ctx.send(
                embed=Embed(
                    title=f"User found\n{info['name']}",
                    description=f"Rank: {info['rank']}\nTR: {info['tr']}\nIs Eligible for the tournament: True\nBracket: {'u' + '+' if info['rank'].lower() in ('u','x') else 'ss' + '-'}",
                    color=Color.green(),
                )
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Checker(bot, bot.db))
