# This file is a part of TG-FileStreamBot

from aiohttp import web
from .stream_routes import routes

def web_server():
    app = web.Application()
    app.add_routes(routes)
    return app
