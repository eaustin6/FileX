# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import time

__version__ = 2.23
StartTime = time.time()

from .vars import Var
from WebStreamer.bot import StreamBot

__all__ = ["Var", "StreamBot", "StartTime", "__version__"]
