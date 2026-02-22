# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

from urllib.parse import quote_plus
from pyrogram import errors, filters, Client
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from WebStreamer.bot import StreamBot, logger
from WebStreamer.utils.database import db
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
async def media_receive_handler(c: Client, m: Message):
    # Check if user exists in DB
    user = await db.get_user(m.from_user.id)
    if not user:
        if Var.LOCK_MODE:
            await m.reply_text(
                "This bot is in **Lock Mode**.\n"
                "Please use `/login <passkey>` to access the bot."
            )
            return
        else:
            await db.add_user(m.from_user.id)
            user = await db.get_user(m.from_user.id)

    # Check Quota (Soft check)
    if m.from_user.id != Var.OWNER_ID and user['used'] >= user['quota']:
        return await m.reply_text(
            "**Quota Exceeded**\n\n"
            "You have used all your allocated data.\n"
            "Please upgrade your plan using /premium."
        )

    try:
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)

        # Include user_id in hash generation
        file_hash = get_hash(log_msg, Var.HASH_LENGTH, m.from_user.id)

        # Include user_id in the link query parameters
        stream_link = f"{Var.URL}{log_msg.id}/{quote_plus(get_name(m))}?hash={file_hash}&id={m.from_user.id}"
        short_link = f"{Var.URL}{file_hash}{log_msg.id}?id={m.from_user.id}"

        logger.info(f"Generated link: {stream_link} for {m.from_user.first_name}")

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
    except Exception as e:
        logger.error(e)
        await m.reply_text(f"Something went wrong!\n\nError: {e}")
