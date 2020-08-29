import humanize
import logging
from discord import Embed, Color

logger = logging.getLogger(__name__)


class EmojiConfig:
    SILVER_PATRON = (False, 'snailsilver', 553890706045796354)
    GOLD_PATRON = (False, 'snailgold', 553890794453336099)
    PLATINUM_PATRON = (True, 'snailplatinumsp', 555052389820923964)
    DIAMOND_PATRON = (True, 'snaildiamondsp', 555052389606883351)
    LEGENDARY_PATRON = (True, 'snaillegendarysp', 555052390261325845)

    @staticmethod
    def get_patron_emoji(tier):
        try:
            animated, name, id = getattr(EmojiConfig, '{}_PATRON'.format(tier.upper()))
            return '<{}:{}:{}>'.format('a' if animated else '', name, id)
        except:
            pass

        return ''


class DiscordBotUtils:
    @staticmethod
    def parse_query(message, q):
        discord_id, steam_id, steam_custom_id = None, None, None
        if q:
            if '@' in q:
                discord_id = True
                q = q[3:-1]
            elif len(q) == 17 and q.isnumeric():
                steam_id = True
            else:
                steam_custom_id = True
        else:
            discord_id = True
            q = message.author.id

        logger.info('')
        return discord_id, steam_id, steam_custom_id, q

    @staticmethod
    def create_user_base_embed(api_response):
        """
        Creates a base embed used as base for profile and ranking commands
        :param api_response: response/data from the API
        :return: Embed used as base for ranking and profile command
        """

        country_code = api_response['steam']['extra']['country_code']
        description = None

        if country_code:
            country_name = api_response['steam']['extra']['country_name']
            region_name = api_response['steam']['extra']['region_name']
            region_url_name = api_response['steam']['extra']['region_url_name']

            country_emoji = ':flag_{}:'.format(country_code.lower())
            country_name = '[{}]({}), [{}]({})'.format(
                country_name,
                'https://www.steamladder.com/ladder/xp/{}'.format(country_code.lower()),
                region_name,
                'https://www.steamladder.com/ladder/xp/{}'.format(region_url_name),
            )

            description = '{} {}'.format(country_emoji, country_name)

        color = Color(value=0x5e70e4)
        if api_response['steamladder']['settings']['custom_name_color']:
            color = int(api_response['steamladder']['settings']['custom_name_color'], 16)

        embed = Embed(description=description, color=color)
        embed.set_thumbnail(url=api_response['steam']['avatar']['full'])
        embed.set_author(
            name=api_response['steam']['name'],
            url='https://steamladder.com/profile/{}'.format(api_response['steam']['id']),
            icon_url=api_response['steam']['avatar']['default']
        )

        is_patreon = api_response['steamladder']['patreon']['active']
        if is_patreon:
            patreon_tier = api_response['steamladder']['patreon']['tier']
            embed.add_field(name='Patron', value='{} **{} Supporter**'.format(EmojiConfig.get_patron_emoji(patreon_tier), patreon_tier), inline=False)
       
        is_private_profile = api_response['steam']['is_private_profile']
        if is_private_profile:
            embed.add_field(name='Profile status', value=':lock: Private', inline=False)

        return embed

    @staticmethod
    def create_profile_embed(embed, api_response):
        """
        Embed with user profile data
        :param embed: base embed from create_user_base_embed()
        :param api_response: response from steamladder api
        :return: Embed
        """

        # Stats
        if api_response['steam']['extra']['level']:
            embed.add_field(name='Level', value=api_response['steam']['extra']['level'], inline=True)

        if api_response['steam']['extra']['playtime_min']:
            embed.add_field(name='Playtime', value='{}h'.format(int(api_response['steam']['extra']['playtime_min'] / 60)), inline=True)
        else:
            embed.add_field(name='Playtime', value=':lock: Private', inline=True)

        if api_response['steam']['extra']['games']:
            embed.add_field(name='Games', value=api_response['steam']['extra']['games'], inline=True)
        else:
            embed.add_field(name='Games', value=':lock: Private', inline=True)

        # Ranks
        if api_response['steamladder']['ranking']['worldwide']['xp']:
            embed.add_field(name='Level rank', value='{}'.format(api_response['steamladder']['ranking']['worldwide']['xp']), inline=True)
            embed.add_field(name='Playtime rank', value='{}'.format(api_response['steamladder']['ranking']['worldwide']['playtime']), inline=True)
            embed.add_field(name='Games rank', value='{}'.format(api_response['steamladder']['ranking']['worldwide']['games']), inline=True)

        # Most played game (first in array of most played games)
        if len(api_response['steam']['extra']['most_played']) > 0:
            embed.add_field(
                name='Most played game',
                value='[{}]({}) ({}h)'.format(
                    api_response['steam']['extra']['most_played'][0]['name'],
                    'https://www.steamladder.com/ladder/playtime/{}'.format(api_response['steam']['extra']['most_played'][0]['id']),
                    int(api_response['steam']['extra']['most_played'][0]['playtime_min'] / 60)
                ),
                inline=False
            )

        return embed

    @staticmethod
    def create_rank_embed(embed, api_response):
        """
        Embed with data about user ranking
        :param embed: base embed from create_user_base_embed()
        :param api_response: response from steamladder api
        :return: Embed
        """

        embed.add_field(name='W / R / N', value='**W**orldwide, **R**egional, **N**ational', inline=False)

        # XP Ranking
        if api_response['steamladder']['ranking']['worldwide']['xp']:
            embed.add_field(name='Level (W)', value=api_response['steamladder']['ranking']['worldwide']['xp'], inline=True)

            if api_response['steamladder']['ranking']['regional']['xp']:
                embed.add_field(name='Level (R)', value=api_response['steamladder']['ranking']['regional']['xp'], inline=True)

            if api_response['steamladder']['ranking']['national']['xp']:
                embed.add_field(name='Level (N)', value=api_response['steamladder']['ranking']['national']['xp'], inline=True)

        # Playtime Ranking
        if api_response['steamladder']['ranking']['worldwide']['playtime']:
            embed.add_field(name='Playtime (W)', value=api_response['steamladder']['ranking']['worldwide']['playtime'], inline=True)

            if api_response['steamladder']['ranking']['regional']['playtime']:
                embed.add_field(name='Playtime (R)', value=api_response['steamladder']['ranking']['regional']['playtime'], inline=True)

            if api_response['steamladder']['ranking']['national']['playtime']:
                embed.add_field(name='Playtime (N)', value=api_response['steamladder']['ranking']['national']['playtime'], inline=True)

        # Games Ranking
        if api_response['steamladder']['ranking']['worldwide']['games']:
            embed.add_field(name='Games (W)', value=api_response['steamladder']['ranking']['worldwide']['games'], inline=True)

            if api_response['steamladder']['ranking']['regional']['games']:
                embed.add_field(name='Games (R)', value=api_response['steamladder']['ranking']['regional']['games'], inline=True)

            if api_response['steamladder']['ranking']['national']['games']:
                embed.add_field(name='Games (N)', value=api_response['steamladder']['ranking']['national']['games'], inline=True)

        return embed

    @staticmethod
    def create_value_embed(embed, api_response):
        """
        Embed with data about profile value
        :param embed: base embed from create_user_base_embed()
        :param api_response: response from steamladder api
        :return: Embed
        """

        values = api_response['steamladder']['value']

        total_value = 0
        total_value += values['level'] if values['level'] else 0
        total_value += values['games_current'] if values['games_current'] else 0
        total_value += values['donator_value'] if values['donator_value'] else 0

        if total_value > 0:
            embed.add_field(name='Total value', value='**${}**'.format(humanize.intcomma(round(total_value))), inline=False)

            if values['level']:
                embed.add_field(name='Level value', value='${}'.format(humanize.intcomma(round(values['level']))), inline=True)

            if values['games_current']:
                embed.add_field(name='Games value', value='${}'.format(humanize.intcomma(round(values['games_current']))), inline=True)

            donator_value = values['donator_value'] if values['donator_value'] else 0
            embed.add_field(name='Donator value', value='${}'.format(humanize.intcomma(round(donator_value))), inline=True)
        else:
            embed.add_field(name='Info', value='No value known, try updating your profile.', inline=False)

        embed.set_footer(text='Game pricing data based on current Steam store prices.')
        return embed

    @staticmethod
    def create_profile_status(embed, api_response):
        """
        Embed with user profile status
        :param embed: base embed from create_user_base_embed()
        :param api_response: response from steamladder api
        :return: Embed
        """

        if not api_response['steam']['is_private_profile']:
            embed.add_field(name='Profile status', value=':green_circle: Public', inline=False)

        if api_response['steam']['extra']['games']:
            embed.add_field(name='Games', value=':green_circle: Public', inline=True)
        else:
            embed.add_field(name='Games', value=':lock: Private', inline=True)

        if api_response['steam']['extra']['playtime_min']:
            embed.add_field(name='Playtime', value=':green_circle: Public', inline=True)
        else:
            embed.add_field(name='Playtime', value=':lock: Private', inline=True)

        if api_response['steam']['extra']['is_community_banned']:
            embed.add_field(name='Community', value=':red_circle: Banned', inline=True)
        else:
            embed.add_field(name='Community', value=':green_circle: Not banned', inline=True)

        if api_response['steam']['extra']['economy_status'] == 'none':
            embed.add_field(name='Trading', value=':green_circle: Can trade', inline=True)
        else:
            embed.add_field(name='Trading', value=':red_circle: {}'.format(api_response['steam']['extra']['economy_status']), inline=True)

        if api_response['steam']['extra']['is_vac_banned']:
            embed.add_field(name='VAC', value=':red_circle: Banned', inline=True)
        else:
            embed.add_field(name='VAC', value=':green_circle: Not banned', inline=True)

        if api_response['steam']['extra']['game_bans'] > 0:
            embed.add_field(name='Game bans', value=':red_circle: {} bans'.format(api_response['steam']['extra']['game_bans']), inline=True)
        else:
            embed.add_field(name='Game bans', value=':green_circle: Not banned', inline=True)

        return embed
