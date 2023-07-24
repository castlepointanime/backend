import json


class Config():

    def __init__(self) -> None:
        with open('./config.json', 'r') as config_file:
            self._config = json.load(config_file)

    def get_contract_limit(self, key: str) -> int:
        value = self._config['contract_limits'].get(key)
        assert type(value) == int, "Invalid config file. Contract limits can only be integers."
        return value
