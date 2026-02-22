# This file is a part of TG-FileStreamBot
# Coding : Owner

import time

__version__ = 2.23
StartTime = time.time()

from .vars import Var  # noqa: E402
from WebStreamer.bot import StreamBot  # noqa: E402

__all__ = ["Var", "StreamBot", "StartTime", "__version__"]
