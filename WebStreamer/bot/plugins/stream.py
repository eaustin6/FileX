# This file is a part of TG-FileStreamBot

from urllib.parse import quote_plus

from pyrogram import errors, filters
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from WebStreamer.bot import StreamBot, logger, authorized_users
from WebStreamer.utils import get_hash, get_name
from WebStreamer.utils.database import db
from WebStreamer.utils.file_properties import get_media_from_message
from WebStreamer.vars import Var


@StreamBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.audio
        | filters.animation
        | filters.voice
        | filters.video_note
        | filters.photo
        | filters.sticker
    ),
    group=4,
)
async def media_receive_handler(_, m: Message):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)

    # Lock Mode Check
    if Var.LOCK_MODE:
        user = await db.get_user(m.from_user.id)
        if not user or not user.get('authorized', False):
             if not (str(m.from_user.id) in Var.ALLOWED_USERS or m.from_user.username in Var.ALLOWED_USERS or m.from_user.id == Var.OWNER_ID):
                return await m.reply(
                    "This bot is in **Lock Mode**. Please authorize yourself using `/login <passkey>`.",
                    quote=True
                )

    # Quota Check
    if m.from_user.id != Var.OWNER_ID:
        user = await db.get_user(m.from_user.id)
        traffic_used = user.get('traffic_used', 0)
        traffic_limit = user.get('traffic_limit', 0)

        # If limit is 0, user has no quota.
        if traffic_limit == 0:
            return await m.reply(
                "You have 0 usage quota. Please contact the owner to purchase credits.",
                quote=True
            )

        if traffic_used >= traffic_limit:
            return await m.reply(
                f"You have exceeded your traffic limit of {traffic_limit} bytes.\n"
                f"Used: {traffic_used} bytes.\n"
                f"Please contact owner to increase quota.",
                quote=True
            )

        # Update usage (approximate by file size)
        media = get_media_from_message(m)
        if isinstance(media, list):
            file_size = getattr(media[-1], "file_size", 0)
        else:
            file_size = getattr(media, "file_size", 0)

        if file_size > 0:
            await db.update_user_usage(m.from_user.id, file_size)

    log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
    file_hash = get_hash(log_msg, Var.HASH_LENGTH)
    stream_link = f"{Var.URL}{log_msg.id}/{quote_plus(get_name(m))}?hash={file_hash}"
    short_link = f"{Var.URL}{file_hash}{log_msg.id}"
    logger.info(f"Generated link: {stream_link} for {m.from_user.first_name}")

    try:
        await m.reply_text(
            text="<code>{}</code>\n(<a href='{}'>shortened</a>)".format(
                stream_link, short_link
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🔴 Download Link", url=stream_link)],
                    [InlineKeyboardButton("🟢 Watch Online", url=stream_link)],
                    [InlineKeyboardButton("🔵 Short Link", url=short_link)]
                ]
            ),
        )
    except errors.ButtonUrlInvalid:
        await m.reply_text(
            text="<code>{}</code>\n\nshortened: {})".format(
                stream_link, short_link
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
        )
