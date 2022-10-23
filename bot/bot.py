import discord
from discord import app_commands
from api import APIException, SteamLadderAPI
from utils import DiscordBotUtils
from config import DISCORD_ADMIN_USER_IDS, DISCORD_BOT_TOKEN
import logging


class SteamLadderClient(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True


client = SteamLadderClient()
tree = app_commands.CommandTree(client)
group = app_commands.Group(name="sl", description="SteamLadder Group")


@group.command(name="rank", description="Get the users rank")
async def self(interaction: discord.Interaction, steam_id: str, update: bool = False):
    force_update = update and interaction.user.id in DISCORD_ADMIN_USER_IDS

    await interaction.response.defer(ephemeral=True)

    try:
        api_response = await SteamLadderAPI.get_profile(author_id=interaction.user.id, q=steam_id, update=update, force_update=force_update)
        base_embed = DiscordBotUtils.create_user_base_embed(api_response)
        rank_embed = DiscordBotUtils.create_value_embed(base_embed, api_response)
        await interaction.followup.send(embed=rank_embed)
    except APIException as e:
        await interaction.followup.send(e)


@group.command(name="value", description="View value stats of a user")
async def self(interaction: discord.Interaction, steam_id: str, update: bool = False):
    force_update = update and interaction.user.id in DISCORD_ADMIN_USER_IDS

    await interaction.response.defer(ephemeral=True)

    try:
        api_response = await SteamLadderAPI.get_profile(author_id=interaction.user.id, q=steam_id, update=update, force_update=force_update)
        base_embed = DiscordBotUtils.create_user_base_embed(api_response)
        rank_embed = DiscordBotUtils.create_value_embed(base_embed, api_response)
        await interaction.followup.send(embed=rank_embed)
    except APIException as e:
        await interaction.followup.send(e)


@group.command(name="profile", description="View a profile summary of a user")
async def self(interaction: discord.Interaction, steam_id: str, update: bool = False):
    force_update = update and interaction.user.id in DISCORD_ADMIN_USER_IDS

    await interaction.response.defer(ephemeral=True)

    try:
        api_response = await SteamLadderAPI.get_profile(author_id=interaction.user.id, q=steam_id, update=update, force_update=force_update)
        base_embed = DiscordBotUtils.create_user_base_embed(api_response)
        profile_embed = DiscordBotUtils.create_profile_status(base_embed, api_response)
        await interaction.followup.send(embed=profile_embed)
    except APIException as e:
        await interaction.followup.send(e)


@group.command(name="admin", description="Administrator commands")
async def self(interaction: discord.Interaction, command: str):

    if interaction.user.id not in DISCORD_ADMIN_USER_IDS:
        return

    if command == 'guilds':
        servers = sorted(client.guilds, key=lambda g: g.member_count, reverse=True)
        servers = ['{} | Members: {}'.format(server.name, server.member_count) for server in servers]
        servers_str = "\n".join(servers)
        await interaction.response.send_message('I am in {} servers!'.format(len(servers)))


@group.command(name="invite", description="Add this bot to your server")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message('Add me to your server: <https://steamladder.com/bot/>')


@group.command(name="github", description="Get Github repository")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message('View code on Github: <https://github.com/bommels/SteamLadderBot>')


@group.command(name="join", description="Join the SteamLadder Discord server")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message('Join the Steam Ladder server: https://discord.gg/C4pdK7Z')


@group.command(name="privacy", description="Get the Privacy Policy URL")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message('View our Privacy Policy: <https://steamladder.com/support/privacy>')

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s', level=logging.INFO)
    tree.add_command(group)
    client.run(DISCORD_BOT_TOKEN)
