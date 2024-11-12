import logging
import os

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)

load_dotenv()

sentry_sdk.init(dsn=os.getenv("SENTRY"), integrations=[sentry_logging])
