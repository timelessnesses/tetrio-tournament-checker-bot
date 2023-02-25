import asyncpg
from discord.ext.commands import bot
from dotenv import load_dotenv
from discord import Intents

load_dotenv()
import asyncio
import os
import logging
logging.basicConfig(level=logging.DEBUG)

bot = bot.Bot("c!", intents=Intents.all())


async def main():
    bot.db = await asyncpg.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    await bot.load_extension("cogs.checker")
    await bot.load_extension("cogs.help")
    await bot.start(os.getenv("TOKEN"))


asyncio.run(main())
