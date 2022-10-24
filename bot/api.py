import logging
import requests

from config import STEAMLADDER_API_TOKEN, STEAMLADDER_API_BASE_URL
from utils import DiscordBotUtils

logger = logging.getLogger(__name__)


class APIException(Exception):
    pass


class SteamLadderAPI:
    REQUEST_TIMEOUT_S = 60
    BASE_URL = STEAMLADDER_API_BASE_URL
    BASE_HEADERS = {
        'Authorization': 'Token {}'.format(STEAMLADDER_API_TOKEN)
    }

    @staticmethod
    async def get_profile(author_id, q, update, force_update=False):
        discord_id, steam_id, steam_custom_id, q = DiscordBotUtils.parse_query(author_id, q)
        method = 'discord' if discord_id else 'profile' if steam_id else 'steam'

        if update:
            return SteamLadderAPI._post(version='v2', method='{}/{}'.format(method, q), params={'force': force_update})

        return SteamLadderAPI._get(version='v2', method='{}/{}'.format(method, q), params={'force': force_update})

    @staticmethod
    def handle_response(api_response):
        if api_response.status_code != 200:
            if api_response.status_code == 404:
                raise APIException('Profile not found.')

            try:
                data = api_response.json()
                error_message = data['error'] if 'error' in data else data['detail']
            except Exception as e:
                logger.error(e)
                error_message = 'Unknown error :('

            raise APIException(error_message)

        return api_response.json()

    @staticmethod
    def _post(version, method, params=None):
        logger.info('[POST] {} (params {})'.format(method, params))

        try:
            return SteamLadderAPI.handle_response(
                requests.post(
                    url='{}/{}/{}/'.format(SteamLadderAPI.BASE_URL, version, method),
                    headers=SteamLadderAPI.BASE_HEADERS,
                    params=params,
                    timeout=SteamLadderAPI.REQUEST_TIMEOUT_S
                )
            )
        except requests.Timeout:
            raise APIException('Steam Ladder is busy.. try again later.')
        except requests.RequestException:
            raise APIException('I could not process this request.')

    @staticmethod
    def _get(version, method, params=None):
        logger.info('[GET] {} (params {})'.format(method, params))

        try:
            return SteamLadderAPI.handle_response(
                requests.get(
                    url='{}/{}/{}/'.format(SteamLadderAPI.BASE_URL, version, method),
                    headers=SteamLadderAPI.BASE_HEADERS,
                    params=params,
                    timeout=SteamLadderAPI.REQUEST_TIMEOUT_S
                )
            )
        except requests.Timeout:
            raise APIException('Steam Ladder is busy.. try again later.')
        except requests.RequestException:
            raise APIException('I could not process this request.')
