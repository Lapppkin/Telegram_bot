import importlib
import os
import sys
from logging import getLogger

# TG_TOKEN = '1054775144:AAGR0Pu07k2Ql7VdhleiKL1bl79J6keAEfA'
# TG_API_URL = 'https://telegg.ru/orig/bot'

logger = getLogger(__name__)


def load_config():
    conf_name = os.environ.get("TG_CONF")
    if conf_name is None:
        conf_name = "development"
    try:
        r = importlib.import_module("settings.{}".format(conf_name))
        logger.debug("Loaded config \"{}\" - OK".format(conf_name))
        return r
    except (TypeError, ValueError, ImportError):
        logger.error("Invalid config \"{}\"".format(conf_name))
        sys.exit(1)

