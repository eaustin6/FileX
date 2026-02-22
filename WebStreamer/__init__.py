# This file is a part of TG-FileStreamBot

import time

__version__ = 3.0
StartTime = time.time()

from .vars import Var  # noqa: E402
from WebStreamer.bot import StreamBot  # noqa: E402

__all__ = ["Var", "StreamBot", "StartTime", "__version__"]
