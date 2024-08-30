from aiogram import BaseMiddleware, types
from aiogram.client.bot import Bot
from typing import Callable, Any, Awaitable, Dict

class AccessMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot, latest_messages: Dict[int, tuple]):
        self.bot = bot
        self.latest_messages = latest_messages
        super().__init__()

    async def __call__(self, handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]], event: types.Message, data: Dict[str, Any]) -> Any:
        data['bot'] = self.bot
        data['latest_messages'] = self.latest_messages
        return await handler(event, data)