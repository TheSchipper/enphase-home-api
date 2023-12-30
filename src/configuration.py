import json


class EnphaseConfiguration:
    """
    Keep track of local configuration file
    """
    def __init__(self, file_path="enphase-configuration.json"):
        self.file_path = file_path

    def check_configuration_file(self, config_path):
        """

        :return:
        """
        with open(config_path, 'r') as f:
            return json.loads(f.read())

    def update_tokens(self, access_token, refresh_token):
        with open("enphase-configuration.json", "rw+") as f:
            contents = json.loads(f.read())
            contents["ENPHASE_ACCESS_TOKEN"] = access_token
            contents["ENPHASE_REFRESH_TOKEN"] = refresh_token
            f.write(contents)
