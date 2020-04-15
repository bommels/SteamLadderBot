from discord import Embed, Color


class DiscordBotUtils:
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

        if api_response['steam']['is_private_profile']:
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
