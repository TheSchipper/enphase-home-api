import aiohttp
import base64
import logging
import os

from dotenv import load_dotenv


ENPHASE_API_URL = "https://api.enphaseenergy.com/api/v4/systems"

logger = logging.getLogger(__name__)


class EnphaseAPIClient:
    """
    Simple wrapper for Enphase V4 API
    """

    def __init__(self):
        load_dotenv()
        self.ho_code = os.environ["ENPHASE_CODE"]
        self.client_id = os.environ["ENPHASE_CLIENT_ID"]
        self.client_secret = os.environ["ENPHASE_CLIENT_SECRET"]
        self.api_key = os.environ["ENPHASE_API_KEY"]
        self.system_id = os.environ["ENPHASE_SYSTEM_ID"]
        self.refresh_token = os.environ["ENPHASE_REFRESH_TOKEN"]
        self.access_token = os.environ["ENPHASE_ACCESS_TOKEN"]

    async def generate_enphase_access_token(
        self, session: aiohttp.ClientSession
    ) -> tuple[str, str]:
        """
        Get the access token the first time using the homeowner code (ho_code), the App client ID (client_id)
        and the App client secret (client_secret). This will also provide the new refresh token. If the user has
        already provided an access token and refresh token, then it is recommended to skip using this method and
        just refresh the tokens (~EnphaseAPI.generate_new_enphase_tokens) when needed.

        :return:
         * access token
         * refresh token
        """
        url = (
            "https://api.enphaseenergy.com/oauth/token?grant_type=authorization_code&redirect_uri"
            f"=https://api.enphaseenergy.com/oauth/redirect_uri&code={self.ho_code}"
        )
        basic_auth_token = base64.b64encode(
            bytes(f"{self.client_id}:{self.client_secret}", "utf-8")
        ).decode("utf-8")
        headers = {"Authorization": f"Basic {basic_auth_token}"}
        async with session.post(url, headers=headers) as resp:
            resp_json = await resp.json()
            logger.debug(f"Response: {resp_json}")
            return resp_json["access_token"], resp_json["refresh_token"]

    async def generate_new_enphase_tokens(
        self, session: aiohttp.ClientSession
    ) -> tuple[str, str]:
        """
        Refresh the access and refresh tokens.

        :return:
         * access token
         * refresh token
        """
        url = (
            "https://api.enphaseenergy.com/oauth/token?grant_type=refresh_token"
            f"&refresh_token={self.refresh_token}"
        )
        logger.debug(f"Refreshing tokens. URL: {url}")
        basic_auth_token = base64.b64encode(
            bytes(f"{self.client_id}:{self.client_secret}", "utf-8")
        ).decode("utf-8")
        headers = {"Authorization": f"Basic {basic_auth_token}"}
        async with session.post(url, headers=headers) as resp:
            resp_json = await resp.json()
            print(f"Response: {resp_json}")
            logger.debug(f"Response: {resp_json}")
            return resp_json["access_token"], resp_json["refresh_token"]

    async def get_enphase_system_information(
        self, session: aiohttp.ClientSession
    ) -> str:
        """
        Return the system information

        GET /api/v4/systems/{system_id}
        """
        endpoint = self.system_id
        url = f"{ENPHASE_API_URL}/{endpoint}?key={self.api_key}"
        logger.debug(f"Getting system information. URL: {url}")
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with session.get(url, headers=headers) as resp:
            resp_json = await resp.json()
            logger.debug(f"Response: {resp_json}")
            return resp_json

    async def get_system_summary_from_enphase(
        self, session: aiohttp.ClientSession
    ) -> str:
        """
        Return the system summary for today.

        GET /api/v4/systems/{system_id}/summary
        """
        endpoint = "summary"
        url = f"{ENPHASE_API_URL}/{self.system_id}/{endpoint}?key={self.api_key}"
        logger.debug(f"Getting system summary. URL: {url}")
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with session.get(url, headers=headers) as resp:
            resp_json = await resp.json()
            logger.debug(f"Response: {resp_json}")
            return resp_json

    async def get_system_devices_from_enphase(
        self, session: aiohttp.ClientSession
    ) -> str:
        """
        Return the system's devices

        GET /api/v4/systems/{system_id}/devices
        """
        endpoint = "devices"
        url = f"{ENPHASE_API_URL}/{self.system_id}/{endpoint}?key={self.api_key}"
        logger.debug(f"Getting system devices. URL: {url}")
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with session.get(url, headers=headers) as resp:
            resp_json = await resp.json()
            logger.debug(f"Response: {resp_json}")
            return resp_json
