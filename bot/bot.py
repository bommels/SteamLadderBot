import logging

from discord import Activity, ActivityType
from discord.ext import commands

from config import DISCORD_COMMAND_PREFIX, DISCORD_ADMIN_USER_IDS, DISCORD_BOT_TOKEN
from api import SteamLadderAPI, APIException
from utils import DiscordBotUtils

logger = logging.getLogger(__name__)
bot = commands.Bot(command_prefix=DISCORD_COMMAND_PREFIX)


@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))
    await bot.change_presence(activity=Activity(name='SteamLadder.com', type=ActivityType.watching))


@bot.command()
async def value(ctx, steam_id=None, update=None):
    """View value stats of a user."""
    discord_id = steam_id[3:-1] if steam_id and '@' in steam_id else ctx.message.author.id if steam_id is None else None
    steam_id = None if discord_id else steam_id

    update = update and update == 'update'
    force_update = update and ctx.message.author.id in DISCORD_ADMIN_USER_IDS

    if update:
        message = await ctx.send('Updating profile..')

    logger.info('Received !value command with params steam_id {}, discord_id {}, update: {}, force_update: {}'.format(
        steam_id, discord_id, update, force_update
    ))

    try:
        api_response = SteamLadderAPI.get_profile(steam_id=steam_id, discord_id=discord_id, update=update, force_update=force_update)
        base_embed = DiscordBotUtils.create_user_base_embed(api_response)
        rank_embed = DiscordBotUtils.create_value_embed(base_embed, api_response)
        await ctx.send(embed=rank_embed)
    except APIException as e:
        await ctx.send(e)

    if update:
        await message.delete()

@bot.command()
async def rank(ctx, steam_id=None, update=None):
    """View ranking stats of a user."""
    discord_id = steam_id[3:-1] if steam_id and '@' in steam_id else ctx.message.author.id if steam_id is None else None
    steam_id = None if discord_id else steam_id
    update = update and update == 'update'
    force_update = update and ctx.message.author.id in DISCORD_ADMIN_USER_IDS

    if update:
        message = await ctx.send('Updating profile..')

    logger.info('Received !rank command with params steam_id {}, discord_id {}, update: {}, force_update: {}'.format(
        steam_id, discord_id, update, force_update
    ))

    try:
        api_response = SteamLadderAPI.get_profile(steam_id=steam_id, discord_id=discord_id, update=update, force_update=force_update)
        base_embed = DiscordBotUtils.create_user_base_embed(api_response)
        rank_embed = DiscordBotUtils.create_rank_embed(base_embed, api_response)
        await ctx.send(embed=rank_embed)
    except APIException as e:
        await ctx.send(e)

    if update:
        await message.delete()


@bot.command()
async def profile(ctx, steam_id=None, update=None):
    """View a profile summary of a user."""
    discord_id = steam_id[3:-1] if steam_id and '@' in steam_id else ctx.message.author.id if steam_id is None else None
    steam_id = None if discord_id else steam_id
    update = update and update == 'update'
    force_update = update and ctx.message.author.id in DISCORD_ADMIN_USER_IDS

    if update:
        message = await ctx.send('Updating profile..')

    logger.info('Received !profile command with params steam_id {}, discord_id {}, update: {}, force_update: {}'.format(
        steam_id, discord_id, update, force_update
    ))

    try:
        api_response = SteamLadderAPI.get_profile(steam_id=steam_id, discord_id=discord_id, update=update, force_update=force_update)
        base_embed = DiscordBotUtils.create_user_base_embed(api_response)
        profile_embed = DiscordBotUtils.create_profile_embed(base_embed, api_response)
        await ctx.send(embed=profile_embed)
    except APIException as e:
        await ctx.send(e)

    if update:
        await message.delete()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s', level=logging.INFO)
    bot.run(DISCORD_BOT_TOKEN)
