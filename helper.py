from __future__ import annotations

import multiprocessing

from datetime import datetime
from os import environ
from typing import Any, Generic, TypeVar

import gunicorn.app.base

from gunicorn.config import Config as GunicornConfig
from pydantic import BaseModel, root_validator

T = TypeVar("T")


def log(msg: str) -> None:
    """log helper. Replace with some more sophisticated logging if needed."""
    # Maybe this at some point: https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/
    tag = f"{str(datetime.now())[:19]}"
    print(f"[{tag}]: {msg}")


def f2s(filename: str) -> str:
    """Really simple helper to convert file to string."""
    with open(filename, "r", encoding="utf-8") as file:
        return "".join(file.readlines())


class StandaloneApplication(  # pylint: disable=W0223
    Generic[T], gunicorn.app.base.BaseApplication
):
    def __init__(self, app: T, options: dict | None = None):
        self.options = options or {}
        self.application = app
        self.cfg: GunicornConfig = GunicornConfig()
        super().__init__()

    def load_config(self) -> None:
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> T:
        return self.application


class ConfigProps(BaseModel):
    ketcher_url: str = "http://chemotion/ketcher"
    scriptfile: str = "./script.js"
    port: int = 9000
    debug_mode: bool = False
    cors_allowed_origins: list = [
        "*",
        "http://localhost",
        "http://localhost:9000",
    ]
    max_workers = multiprocessing.cpu_count()

    @classmethod
    def from_env(cls, prefix: str = "CONFIG_") -> ConfigProps:
        """Load config from environment variables."""

        config_props = cls()
        for key, field in cls.__fields__.items():
            osvar = f"{prefix}{key.upper()}"
            val: Any = environ.get(osvar)

            if not val:
                continue

            if field.type_ == list:
                val = val.split(",")
            elif field.type_ == int:
                val = int(val)

            setattr(config_props, key, val)
        return config_props


class Configuration(ConfigProps):
    script: str = ""

    def __init__(self, config: ConfigProps):
        super().__init__(**config.dict())

    @root_validator()
    def root_validator(cls, values: dict) -> dict:  # pylint: disable=no-self-argument
        values["script"] = f2s(values["scriptfile"])
        return values
