import logging

from discord import Activity, ActivityType
from discord.ext import commands

from config import DISCORD_COMMAND_PREFIX, DISCORD_ADMIN_USER_IDS, DISCORD_BOT_TOKEN
from api import SteamLadderAPI, APIException
from utils import DiscordBotUtils

logger = logging.getLogger(__name__)
bot = commands.Bot(command_prefix=DISCORD_COMMAND_PREFIX)


class SteamLadderCommands(commands.Cog):
    """Steam Ladder stats commands"""
    qualified_name = 'General'

    @commands.command()
    async def value(self, ctx, steam_id=None, update=None):
        """View value stats of a user"""
        update = update and update == 'update'
        force_update = update and ctx.message.author.id in DISCORD_ADMIN_USER_IDS

        if update:
            message = await ctx.send('Updating profile..')

        logger.info('Received !value command with params steam_id {}, update: {}, force_update: {}'.format(
            steam_id, update, force_update
        ))

        try:
            api_response = SteamLadderAPI.get_profile(message=ctx.message, q=steam_id, update=update, force_update=force_update)
            base_embed = DiscordBotUtils.create_user_base_embed(api_response)
            rank_embed = DiscordBotUtils.create_value_embed(base_embed, api_response)
            await ctx.send(embed=rank_embed)
        except APIException as e:
            await ctx.send(e)

        if update:
            await message.delete()

    @commands.command()
    async def rank(self, ctx, steam_id=None, update=None):
        """View ranking stats of a user"""
        update = update and update == 'update'
        force_update = update and ctx.message.author.id in DISCORD_ADMIN_USER_IDS

        if update:
            message = await ctx.send('Updating profile..')

        logger.info('Received !rank command with params steam_id {}, update: {}, force_update: {}'.format(
            steam_id, update, force_update
        ))

        try:
            api_response = SteamLadderAPI.get_profile(message=ctx.message, q=steam_id, update=update, force_update=force_update)
            base_embed = DiscordBotUtils.create_user_base_embed(api_response)
            rank_embed = DiscordBotUtils.create_rank_embed(base_embed, api_response)
            await ctx.send(embed=rank_embed)
        except APIException as e:
            await ctx.send(e)

        if update:
            await message.delete()

    @commands.command()
    async def profile(self, ctx, steam_id=None, update=None):
        """View a profile summary of a user"""
        update = update and update == 'update'
        force_update = update and ctx.message.author.id in DISCORD_ADMIN_USER_IDS

        if update:
            message = await ctx.send('Updating profile..')

        logger.info('Received !profile command with params steam_id {}, update: {}, force_update: {}'.format(
            steam_id, update, force_update
        ))

        try:
            api_response = SteamLadderAPI.get_profile(message=ctx.message, q=steam_id, update=update, force_update=force_update)
            base_embed = DiscordBotUtils.create_user_base_embed(api_response)
            profile_embed = DiscordBotUtils.create_profile_embed(base_embed, api_response)
            await ctx.send(embed=profile_embed)
        except APIException as e:
            await ctx.send(e)

        if update:
            await message.delete()

    @commands.command()
    async def status(self, ctx, steam_id=None, update=None):
        """View profile status of a user"""
        update = update and update == 'update'
        force_update = update and ctx.message.author.id in DISCORD_ADMIN_USER_IDS

        if update:
            message = await ctx.send('Updating profile..')

        logger.info('Received !status command with params steam_id {}, update: {}, force_update: {}'.format(
            steam_id, update, force_update
        ))

        try:
            api_response = SteamLadderAPI.get_profile(message=ctx.message, q=steam_id, update=update, force_update=force_update)
            base_embed = DiscordBotUtils.create_user_base_embed(api_response)
            profile_embed = DiscordBotUtils.create_profile_status(base_embed, api_response)
            await ctx.send(embed=profile_embed)
        except APIException as e:
            await ctx.send(e)

        if update:
            await message.delete()


class MiscCommands(commands.Cog):
    """Misc commands"""
    qualified_name = 'Misc'

    @commands.command()
    async def admin(self, ctx, command):
        """Administrator commands"""
        logger.info('Received !guilds with command {}'.format(command))
        if ctx.message.author.id not in DISCORD_ADMIN_USER_IDS:
            return

        if command == 'guilds':
            servers = sorted(bot.guilds, key=lambda g: g.member_count, reverse=True)
            servers = ['{} | Members: {}'.format(server.name, server.member_count) for server in servers]
            servers_str = "\n".join(servers)
            await ctx.send('I am in {} servers!'.format(len(servers)))

    @commands.command()
    async def invite(self, ctx):
        """Add this bot to your server"""
        logger.info('Received !invite')
        await ctx.send('Add me to your server: <https://steamladder.com/bot/>')

    @commands.command()
    async def github(self, ctx):
        """Get Github repository"""
        logger.info('Received !github')
        await ctx.send('View code on Github: <https://github.com/bommels/SteamLadderBot>')

    @commands.command()
    async def join(self, ctx):
        """Join the SteamLadder Discord server"""
        logger.info('Received !join')
        await ctx.send('Join the Steam Ladder server: https://discord.gg/C4pdK7Z')


@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))
    await bot.change_presence(activity=Activity(name='SteamLadder | !sl help', type=ActivityType.watching))


bot.add_cog(SteamLadderCommands())
bot.add_cog(MiscCommands())

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s', level=logging.INFO)
    bot.run(DISCORD_BOT_TOKEN)
