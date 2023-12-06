from typing import cast
from marshmallow import Schema, post_load, fields
import toml

_CONFIG_FILE = "./task2.conf"
_loaded = False


class ConfigSchema(Schema):
    db_path = fields.String(required=True)
    token_length = fields.Integer(required=True)
    session_timeout_seconds = fields.Integer(required=True)

    @post_load
    def make_config(self, data, **kwargs):
        return Config(**data)


class Config:
    def __init__(self, db_path: str = "", token_length: int = 64,
                 session_timeout_seconds: int = 86400):
        self.db_path = db_path
        self.token_length = token_length
        self.session_timeout_seconds = session_timeout_seconds


def reload():
    global CONFIG
    global _loaded
    conf = toml.load(_CONFIG_FILE)
    schema = ConfigSchema()
    CONFIG = cast(Config, schema.load(conf))
    _loaded = True


CONFIG: Config

if not _loaded:
    reload()
