import asyncio
from typing import Callable, Any, Awaitable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.dispatcher.flags import get_flag
from typing import Any, Awaitable, Callable, Dict
from aiogram.dispatcher.event.handler import HandlerObject
from cachetools import TTLCache

# from bot.const import THROTTLE_TIME_SPIN, THROTTLE_TIME_OTHER

THROTTLE_TIME_SPIN = 1
THROTTLE_TIME_OTHER = 2


class ThrottlingMiddleware(BaseMiddleware):
    caches = {
        "spin": TTLCache(maxsize=10_000, ttl=THROTTLE_TIME_SPIN),
        "default": TTLCache(maxsize=10_000, ttl=THROTTLE_TIME_OTHER)
    }

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any],
    ) -> Any:
        real_handler: HandlerObject = data.get("handler")
        throttling_key = real_handler.flags.get("throttling_key")
        if throttling_key is not None and throttling_key in self.caches:
            if event.from_user.id in self.caches[throttling_key]:
                return
            else:
                self.caches[throttling_key][event.from_user.id] = None
        return await handler(event, data)


class CallbackMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any],
    ) -> Any:
        # await asyncio.sleep(2)
        return await handler(event, data)


class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        self.counter += 1
        # print(event.from_user)
        data['counter'] = self.counter
        return await handler(event, data)


