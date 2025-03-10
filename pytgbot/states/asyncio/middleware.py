from pytgbot.asyncio_handler_backends import BaseMiddleware
from pytgbot.async_pytgbot import AsyncPytgbot
from pytgbot.states.sync.context import StateContext
from pytgbot.util import update_types
from pytgbot import types


class StateMiddleware(BaseMiddleware):

    def __init__(self, bot: AsyncPytgbot) -> None:
        self.update_sensitive = False
        self.update_types = update_types
        self.bot: AsyncPytgbot = bot

    async def pre_process(self, message, data):
        state_context = StateContext(message, self.bot)
        data["state_context"] = state_context
        data["state"] = state_context  # 2 ways to access state context

    async def post_process(self, message, data, exception):
        pass
