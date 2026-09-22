import discord

from akaribot.adapters.discord.client import discord_bot
from akaribot.adapters.discord.slash_parser import slash_parser


@discord_bot.slash_command(name="bilibili", description="Send video ID for video info.")
@discord.option(name="bid", description="Bilibili video ID.")
async def _(ctx: discord.ApplicationContext, bid: str):
    await slash_parser(ctx, bid)
