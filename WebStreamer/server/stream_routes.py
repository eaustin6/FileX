# Taken from megadlbot_oss <https://github.com/eyaadh/megadlbot_oss/blob/master/mega/webserver/routes.py>
# Thanks to Eyaadh <https://github.com/eyaadh>

import logging
import math
import mimetypes
import re
import time
import asyncio

from aiohttp import web
from aiohttp.http_exceptions import BadStatusLine

from WebStreamer import StartTime, StreamBot, Var, __version__, utils
from WebStreamer.bot import multi_clients, work_loads
from WebStreamer.server.exceptions import FIleNotFound, InvalidHash
from WebStreamer.utils.database import db

logger = logging.getLogger("routes")


routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(_):
    uptime = utils.get_readable_time(time.time() - StartTime)
    bot_username = "@" + StreamBot.username
    connected_bots = len(multi_clients)
    total_users = await db.total_users_count()

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TG-FileStreamBot Status</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .card {{ background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }}
            .status-ok {{ color: #10b981; font-weight: bold; }}
            .info-row {{ display: flex; justify-content: space-between; margin: 0.5rem 0; border-bottom: 1px solid #eee; padding-bottom: 0.5rem; }}
            .info-label {{ color: #6b7280; }}
            .info-value {{ font-weight: 500; color: #111827; }}
            h1 {{ margin-top: 0; color: #1f2937; }}
            .footer {{ margin-top: 1.5rem; font-size: 0.875rem; color: #9ca3af; }}
            a {{ color: #3b82f6; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Bot Status</h1>
            <p class="status-ok">● System Operational</p>
            <div class="info-row">
                <span class="info-label">Bot Username</span>
                <span class="info-value"><a href="https://t.me/{StreamBot.username}">{bot_username}</a></span>
            </div>
            <div class="info-row">
                <span class="info-label">Uptime</span>
                <span class="info-value">{uptime}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Connected Bots</span>
                <span class="info-value">{connected_bots}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Total Users</span>
                <span class="info-value">{total_users}</span>
            </div>
             <div class="info-row">
                <span class="info-label">Version</span>
                <span class="info-value">{__version__}</span>
            </div>
            <div class="footer">
                Powered by <a href="https://github.com/Owner/TG-FileStreamBot">TG-FileStreamBot</a>
            </div>
        </div>
    </body>
    </html>
    """
    return web.Response(text=html, content_type='text/html')

@routes.get("/health", allow_head=True)
async def health_check(_):
    return web.Response(text="OK", status=200)

@routes.get(r"/{path:\S+}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        match = re.search(r"^([0-9a-f]{%s})(\d+)$" % (Var.HASH_LENGTH), path)

        user_id_str = request.query.get("id")
        if not user_id_str:
            # Fallback for old links?
            # If completely new format, we enforce ID.
            # But maybe allow if Lock Mode is OFF?
            # No, quota system requires ID.
            # However, if old link doesn't have ID, maybe default to anonymous or owner? No.
            # Let's verify if ID is strictly required.
            raise web.HTTPForbidden(text="Access Denied: User ID missing in link.")

        try:
            user_id = int(user_id_str)
        except ValueError:
             raise web.HTTPForbidden(text="Access Denied: Invalid User ID.")

        if match:
            secure_hash = match.group(1)
            message_id = int(match.group(2))
        else:
            message_id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")

        return await media_streamer(request, message_id, secure_hash, user_id)
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass
    except Exception as e:
        logger.critical(str(e), exc_info=True)
        raise web.HTTPInternalServerError(text=str(e))

class_cache = {}

async def media_streamer(request: web.Request, message_id: int, secure_hash: str, user_id: int):
    # Check User & Quota
    user = await db.get_user(user_id)
    if not user:
         raise web.HTTPForbidden(text="Access Denied: User not registered.")

    if user_id != Var.OWNER_ID and user['used'] >= user['quota']:
         raise web.HTTPForbidden(text="Access Denied: Quota Exceeded. Contact Owner.")

    range_header = request.headers.get("Range", 0)

    index = min(work_loads, key=work_loads.get)
    faster_client = multi_clients[index]

    if Var.MULTI_CLIENT:
        logger.info(f"Client {index} is now serving {request.remote}")

    if faster_client in class_cache:
        tg_connect = class_cache[faster_client]
        logger.debug(f"Using cached ByteStreamer object for client {index}")
    else:
        logger.debug(f"Creating new ByteStreamer object for client {index}")
        tg_connect = utils.ByteStreamer(faster_client)
        class_cache[faster_client] = tg_connect

    file_id = await tg_connect.get_file_properties(message_id)

    # Verify Hash with user_id to ensure link belongs to user
    if utils.get_hash(file_id.unique_id, Var.HASH_LENGTH, user_id) != secure_hash:
        logger.debug(f"Invalid hash for message with ID {message_id} and User {user_id}")
        raise InvalidHash

    file_size = file_id.file_size

    if range_header:
        from_bytes, until_bytes = range_header.replace("bytes=", "").split("-")
        from_bytes = int(from_bytes)
        until_bytes = int(until_bytes) if until_bytes else file_size - 1
    else:
        from_bytes = request.http_range.start or 0
        until_bytes = (request.http_range.stop or file_size) - 1

    if (until_bytes > file_size) or (from_bytes < 0) or (until_bytes < from_bytes):
        return web.Response(
            status=416,
            body="416: Range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )

    chunk_size = 1024 * 1024
    until_bytes = min(until_bytes, file_size - 1)

    offset = from_bytes - (from_bytes % chunk_size)
    first_part_cut = from_bytes - offset
    last_part_cut = until_bytes % chunk_size + 1

    req_length = until_bytes - from_bytes + 1
    part_count = math.ceil(until_bytes / chunk_size) - math.floor(offset / chunk_size)
    body = tg_connect.yield_file(
        file_id, index, offset, first_part_cut, last_part_cut, part_count, chunk_size
    )

    async def monitored_body(body_iterator):
        async for chunk in body_iterator:
            yield chunk
            chunk_len = len(chunk)
            if user_id != Var.OWNER_ID:
                await db.update_user_used(user_id, chunk_len)

    mime_type = file_id.mime_type
    file_name = utils.get_name(file_id)
    disposition = "attachment"

    if not mime_type:
        mime_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"

    if "video/" in mime_type or "audio/" in mime_type or "/html" in mime_type:
        disposition = "inline"

    return web.Response(
        status=206 if range_header else 200,
        body=monitored_body(body),
        headers={
            "Content-Type": f"{mime_type}",
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Length": str(req_length),
            "Content-Disposition": f'{disposition}; filename="{file_name}"',
            "Accept-Ranges": "bytes",
        },
    )
