import base64
import os
import requests
import logging

from enphase_home_api_client.configuration import EnphaseConfiguration

ENPHASE_API_URL = "https://api.enphaseenergy.com/api/v4/systems"

logger = logging.getLogger(__name__)


class EnphaseAPIClient:
    """
    Simple wrapper for Enphase V4 API
    """

    def __init__(self, config_path="enphase-configuration.json"):
        logging.debug(f"Starting Client. Using file path {config_path}")
        #self._set_local_configuration_values(config_path)
        self.ho_code = os.environ["ENPHASE_CODE"]
        self.client_id = os.environ["ENPHASE_CLIENT_ID"]
        self.client_secret = os.environ["ENPHASE_CLIENT_SECRET"]
        self.api_key = os.environ["ENPHASE_API_KEY"]
        self.system_id = os.environ["ENPHASE_SYSTEM_ID"]
        self.refresh_token = os.environ["ENPHASE_REFRESH_TOKEN"]
        self.access_token = os.environ["ENPHASE_ACCESS_TOKEN"]

    def _set_local_configuration_values(self, config_path):
        """

        :return:
        """
        local_configuration = EnphaseConfiguration(config_path)
        configuration = local_configuration.check_configuration_file(config_path)
        self.ho_code = configuration.get("ENPHASE_CODE")
        self.client_id = configuration.get("ENPHASE_CLIENT_ID")
        self.client_secret = configuration.get("ENPHASE_CLIENT_SECRET")
        self.api_key = configuration.get("ENPHASE_API_KEY")
        self.system_id = configuration.get("ENPHASE_SYSTEM_ID")
        self.refresh_token = configuration.get("ENPHASE_REFRESH_TOKEN")
        self.access_token = configuration.get("ENPHASE_ACCESS_TOKEN")

    def generate_enphase_access_token(self):
        """
        Get the access token the first time using the homeowner code (ho_code), the App client ID (client_id)
        and the App client secret (client_secret). This will also provide the new refresh token. If the user has
        already provided an access token and refresh token, then it is recommended to skip using this method and
        just refresh the tokens (~EnphaseAPI.generate_new_enphase_tokens) when needed.

        :return:
         * access token
         * refresh token
        """
        enphase_token_url = (
            "https://api.enphaseenergy.com/oauth/token?grant_type=authorization_code&redirect_uri"
            f"=https://api.enphaseenergy.com/oauth/redirect_uri&code={self.ho_code}"
        )
        self._post_token_request(enphase_token_url)

    def generate_new_enphase_tokens(self):
        """
        Refresh the access and refresh tokens.

        :return:
         * access token
         * refresh token
        """
        enphase_refresh_token_url = (
            "https://api.enphaseenergy.com/oauth/token?grant_type=refresh_token"
            f"&refresh_token={self.refresh_token}"
        )
        logger.debug(f"Refreshing tokens. URL: {enphase_refresh_token_url}")
        self._post_token_request(enphase_refresh_token_url)

    def get_enphase_system_information(self):
        """
        Return the system information

        GET /api/v4/systems/{system_id}
        """
        endpoint = self.system_id
        url = f"{ENPHASE_API_URL}/{endpoint}?key={self.api_key}"
        logger.debug(f"Getting system information. URL: {url}")
        self._post_request(url)

    def get_system_summary_from_enphase(self):
        """
        Return the system summary for today.

        GET /api/v4/systems/{system_id}/summary
        """
        endpoint = "summary"
        url = f"{ENPHASE_API_URL}/{self.system_id}/{endpoint}?key={self.api_key}"
        logger.debug(f"Getting system summary. URL: {url}")
        self._post_request(url)

    def get_system_devices_from_enphase(self):
        """
        Return the system's devices

        GET /api/v4/systems/{system_id}/devices
        """
        endpoint = "devices"
        url = f"{ENPHASE_API_URL}/{self.system_id}/{endpoint}?key={self.api_key}"
        logger.debug(f"Getting system devices. URL: {url}")
        self._post_request(url)

    def _post_token_request(self, url):
        """Makes a POST request to the given URL to get an access token.

        Args:
            url (str): The URL to make the POST request to.

        Returns:
            tuple: A tuple containing:
                access_token (str): The access token returned by the API.
                refresh_token (str): The refresh token returned by the API.

        Raises:
            requests.exceptions.HTTPError: If the API response contains an error.
        """
        basic_auth_token = base64.b64encode(
            bytes(f"{self.client_id}:{self.client_secret}", "utf-8")
        ).decode("utf-8")
        headers = {"Authorization": f"Basic {basic_auth_token}"}
        resp = requests.post(url, headers=headers)
        logger.debug(f"Response: {resp.json()}")
        resp.raise_for_status()
        return resp.json()["access_token"], resp.json()["refresh_token"]

    def _post_request(self, url):
        """Makes a POST request to the given URL.

        Args:
            url (str): The URL to make the POST request to.

        Returns:
            dict: The JSON response data.

        Raises:
            requests.exceptions.HTTPError: If the API response contains an error.
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        resp = requests.post(url, headers=headers)
        logger.debug(f"Response: {resp.json()}")
        resp.raise_for_status()
        return resp.json()
