'''
import os
from os.path import dirname, join
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path, override=True)

# Mpesa
consumer_key = os.environ.get("CONSUMER_KEY", None)
consumer_secret = os.environ.get("CONSUMER_SECRET", None)
accesstoken_url = os.environ.get("ACCESSTOKEN_URL", None)
'''
import os
from os.path import dirname, join
from typing import Tuple
from pydantic import BaseSettings, Field
from pydantic.env_settings import SettingsSourceCallable

dotenv_path = join(dirname(__file__), '.env')


class Settings(BaseSettings):
    consumer_key: str = Field(..., env="CONSUMER_KEY")
    consumer_secret: str = Field(..., env="CONSUMER_SECRET")
    accesstoken_url: str = Field(..., env="ACCESSTOKEN_URL")
    lnm_url: str = Field(..., env="LNM_URL")
    business_shortcode: str = Field(..., env="BUSINESS_SHORTCODE")
    lnm_callback_url: str = Field(..., env="LNM_CALLBACK_URL")
    lnm_passkey: str = Field(..., env="LNM_PASSKEY")

    class Config:
        env_file = dotenv_path
        env_file_encoding = 'utf-8'

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return env_settings, init_settings, file_secret_settings


settings = Settings(_env_file=dotenv_path, _env_file_encoding='utf-8')
