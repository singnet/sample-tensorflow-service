import json
import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

SERVER_PORT = 5001
MINIMUM_SCORE = 0.20
LOG_LEVEL = 10

# Override from file
with open(Path(__file__).parent.parent.joinpath("configuration", "config.json")) as f:
    overrides = json.load(f)
    for k, v in overrides.items():
        logger.debug("overriding config key %s with value %s from config file", k, v)
        setattr(sys.modules[__name__], k, v)

# Override from environment variables
for k in dir(sys.modules[__name__]):
    if os.environ.get(k, None) is not None:
        logger.debug("overriding config key %s with value %s from environment", k, os.environ[k])
        setattr(sys.modules[__name__], k, os.environ[k])
