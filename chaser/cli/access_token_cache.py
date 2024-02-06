import json
import os
from enum import Enum
from typing import Dict
from chaser_util import config


class Region(Enum):
    US = "us"
    CN = "cn"


class AccessTokenCache:
    FILE_PATH = os.path.join(config.config_dir(), "chaser", "access_tokens.json")

    def __init__(self):
        self.access_token_cache = self.load()

    def load(self) -> Dict[str, str]:
        try:
            with open(AccessTokenCache.FILE_PATH, "r") as file:
                data = json.load(file)
                if data is None:  # 处理加载的数据为 None 的情况
                    return {}
                return data
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def add(self, access_token: str, region: Region):
        if self.access_token_cache is None:  # 处理缓存为空的情况
            self.access_token_cache = {}
        self.access_token_cache[region.value] = access_token
        return self

    def get(self, region: Region) -> str:
        return self.access_token_cache.get(region.value, "")

    def save(self):
        os.makedirs(os.path.dirname(AccessTokenCache.FILE_PATH), exist_ok=True)
        try:
            with open(AccessTokenCache.FILE_PATH, "w") as file:
                json.dump(self.access_token_cache, file)
        except Exception as e:
            print(f"Failed to save access token cache: {str(e)}")


token_cache = AccessTokenCache()
