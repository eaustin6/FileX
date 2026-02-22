# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

from urllib.parse import quote_plus

from pyrogram import errors, filters
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from WebStreamer.bot import StreamBot, logger, authorized_users
from WebStreamer.utils import get_hash, get_name
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
    if Var.LOCK_MODE and not (m.from_user.id in authorized_users or str(m.from_user.id) in Var.ALLOWED_USERS or m.from_user.username in Var.ALLOWED_USERS):
        return await m.reply(
            "This bot is in **Lock Mode**. Please authorize yourself using `/login <passkey>`.",
            quote=True
        )

    if Var.ALLOWED_USERS and not ((str(m.from_user.id) in Var.ALLOWED_USERS) or (m.from_user.username in Var.ALLOWED_USERS)):
        return await m.reply("You are not <b>allowed to use</b> this <a href='https://github.com/EverythingSuckz/TG-FileStreamBot'>bot</a>.", quote=True)

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
