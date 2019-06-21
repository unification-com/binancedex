import logging
import os
from enum import Enum
from pathlib import Path

log = logging.getLogger(__name__)


class Environment(Enum):
    LAPTOP = 1
    DOCKER = 2


def get_enum():
    binancedex_env = os.environ.get('binancedex_env')
    if binancedex_env is None:
        return Environment.DOCKER
    else:
        if binancedex_env == 'laptop':
            return Environment.LAPTOP
        if binancedex_env == 'docker':
            return Environment.DOCKER

        raise Exception(f'Unhandled host environment {binancedex_env}')


def reports_store() -> Path:
    environ = get_enum()
    if environ == Environment.LAPTOP:
        return Path('/Users/indika/dev/temp')
    elif environ == Environment.DOCKER:
        return Path('/reports')
    raise Exception(f"Unhandled environment: {environ}")
