from dotenv_settings_handler import BaseSettingsHandler
from dotenv import load_dotenv


class MySettings(BaseSettingsHandler):
    """Settings definition"""
    light_cmd_topic: str
    light_stat_topic: str
    topic:str
    broker = "3.140.85.3"
    port = 1883

    class Config:
        env_prefix = "LC_"

load_dotenv()
settings = MySettings()
