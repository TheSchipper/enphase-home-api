import base64
import requests
import json

ENPHASE_API_URL = "https://api.enphaseenergy.com/api/v4/systems"


def _check_configuration_file():
    """

    :return:
    """
    with open("enphase-configuration.json", 'r') as f:
        return json.loads(f.read())


def _save_refresh_token_locally(refresh_token):
    with open("enphase-refresh-token", 'w') as f:
        f.write(refresh_token)


def _update_tokens(access_token, refresh_token):
    with open("enphase-configuration.json", "rw+") as f:
        contents = json.loads(f.read())
        contents["ENPHASE_ACCESS_TOKEN"] = access_token
        contents["ENPHASE_REFRESH_TOKEN"] = refresh_token
        f.write(contents)


class EnphaseAPI:
    """
    Simple wrapper for Enphase V4 API
    """
    def __init__(self, generate_new_access_token=False):
        configuration = _check_configuration_file()
        self.ho_code = configuration.get("ENPHASE_CODE")
        self.client_id = configuration.get("ENPHASE_CLIENT_ID")
        self.client_secret = configuration.get("ENPHASE_CLIENT_SECRET")
        self.api_key = configuration.get("ENPHASE_API_KEY")
        self.system_id = configuration.get("ENPHASE_SYSTEM_ID")
        self.refresh_token = configuration.get("ENPHASE_REFRESH_TOKEN")
        self.access_token = configuration.get("ENPHASE_ACCESS_TOKEN")

    def get_enphase_access_token(self):
        """
        Get the access token the first time using the home owner code (ho_code), the App client ID (client_id)
        and the App client secret (client_secret). This will also provide the new refresh token. If the user has
        already provided an access token and refresh token, then it is recommended to skip using this method and
         just refresh the tokens (~EnphaseAPI.refresh_tokens) when needed.

        :return:
         * access token
         * refresh token
        """
        enphase_token_url = ("https://api.enphaseenergy.com/oauth/token?grant_type=authorization_code&redirect_uri"
                             f"=https://api.enphaseenergy.com/oauth/redirect_uri&code={self.ho_code}")
        basic_auth_token = base64.b64encode(bytes(f"{self.client_id}:{self.client_secret}", "utf-8")).decode("utf-8")
        headers = {'Authorization': f'Basic {basic_auth_token}'}
        resp = requests.post(enphase_token_url, headers=headers)
        resp.raise_for_status()
        return resp.json()['access_token'], resp.json()['refresh_token']

    def refresh_tokens(self):
        """
        Refresh the access and refresh tokens.

        :return:
         * access token
         * refresh token
        """
        enphase_refresh_token_url = ("https://api.enphaseenergy.com/oauth/token?grant_type=refresh_token"
                                     f"&refresh_token={self.refresh_token}")
        basic_auth_token = base64.b64encode(bytes(f"{self.client_id}:{self.client_secret}", "utf-8")).decode("utf-8")
        headers = {'Authorization': f'Basic {basic_auth_token}'}
        resp = requests.post(enphase_refresh_token_url, headers=headers)
        resp.raise_for_status()
        return resp.json()['access_token'], resp.json()['refresh_token']


    def get_enphase_system_information(self):
        """
        Return the system information

        GET /api/v4/systems/{system_id}

        :return:
        """
        endpoint = self.system_id
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f"{ENPHASE_API_URL}/{endpoint}?key={self.api_key}"
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def get_system_summary_from_enphase(self):
        """
        Return the system summary for today.

        GET /api/v4/systems/{system_id}/summary

        :return:
        """
        endpoint = "summary"
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f'{ENPHASE_API_URL}/{self.system_id}/{endpoint}?key={self.api_key}'
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def get_system_devices_from_enphase(self):
        """
        Return the system's devices

        GET /api/v4/systems/{system_id}/devices

        :return:
        """
        endpoint = "devices"
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f"{ENPHASE_API_URL}/{self.system_id}/{endpoint}?key={self.api_key}"
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()
