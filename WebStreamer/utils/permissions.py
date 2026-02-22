# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

from typing import Optional

from WebStreamer.bot import authorized_users
from WebStreamer.vars import Var


def is_user_locked(user_id: int, username: Optional[str] = None) -> bool:
    """
    Checks if the user is locked out due to LOCK_MODE.
    Returns True if access is denied.
    """
    if Var.LOCK_MODE and not (user_id in authorized_users or str(user_id) in Var.ALLOWED_USERS or (username and username in Var.ALLOWED_USERS)):
        return True
    return False


def is_user_banned(user_id: int, username: Optional[str] = None) -> bool:
    """
    Checks if the user is banned due to ALLOWED_USERS restriction.
    Returns True if access is denied.
    """
    if Var.ALLOWED_USERS and not ((str(user_id) in Var.ALLOWED_USERS) or (username and username in Var.ALLOWED_USERS)):
        return True
    return False
