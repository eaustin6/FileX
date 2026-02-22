# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import sys
from os import environ

from dotenv import load_dotenv

load_dotenv()


class Var:
    MULTI_CLIENT = False
    API_ID = int(environ.get("API_ID", 0))
    API_HASH = str(environ.get("API_HASH", ""))
    BOT_TOKEN = str(environ.get("BOT_TOKEN", ""))
    SLEEP_THRESHOLD = int(environ.get("SLEEP_THRESHOLD", "60"))  # 1 minute
    WORKERS = int(environ.get("WORKERS", "6"))  # 6 workers = 6 commands at once
    BIN_CHANNEL = int(
        environ.get("BIN_CHANNEL", 0)
    )  # you NEED to use a CHANNEL when you're using MULTI_CLIENT
    PORT = int(environ.get("PORT", 8080))
    BIND_ADDRESS = str(environ.get("WEB_SERVER_BIND_ADDRESS", "0.0.0.0"))
    PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
    HAS_SSL = str(environ.get("HAS_SSL", "0").lower()) in ("1", "true", "t", "yes", "y")
    NO_PORT = str(environ.get("NO_PORT", "0").lower()) in ("1", "true", "t", "yes", "y")
    HASH_LENGTH = int(environ.get("HASH_LENGTH", 6))
    if not 5 < HASH_LENGTH < 64:
        sys.exit("Hash length should be greater than 5 and less than 64")
    FQDN = str(environ.get("FQDN", BIND_ADDRESS))
    URL = "http{}://{}{}/".format(
            "s" if HAS_SSL else "", FQDN, "" if NO_PORT else ":" + str(PORT)
        )
    KEEP_ALIVE = str(environ.get("KEEP_ALIVE", "0").lower()) in  ("1", "true", "t", "yes", "y")
    DEBUG = str(environ.get("DEBUG", "0").lower()) in ("1", "true", "t", "yes", "y")
    USE_SESSION_FILE = str(environ.get("USE_SESSION_FILE", "0").lower()) in ("1", "true", "t", "yes", "y")
    ALLOWED_USERS = [x.strip("@ ") for x in str(environ.get("ALLOWED_USERS", "") or "").split(",") if x.strip("@ ")]

    # New variables
    LOCK_MODE = str(environ.get("LOCK_MODE", "0").lower()) in ("1", "true", "t", "yes", "y")
    PASSKEY = str(environ.get("PASSKEY", ""))
    OWNER_ID = int(environ.get("OWNER_ID", "0"))

    if not API_ID:
        print("API_ID variable is missing! Exiting now")
        sys.exit(1)
    if not API_HASH:
        print("API_HASH variable is missing! Exiting now")
        sys.exit(1)
    if not BOT_TOKEN:
        print("BOT_TOKEN variable is missing! Exiting now")
        sys.exit(1)
    if not BIN_CHANNEL:
        print("BIN_CHANNEL variable is missing! Exiting now")
        sys.exit(1)
    if LOCK_MODE and not PASSKEY:
        print("PASSKEY variable is missing! LOCK_MODE is enabled but no PASSKEY provided. Exiting now")
        sys.exit(1)
