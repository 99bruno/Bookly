from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Any, Dict, Awaitable

from app.database.requests.check_user import check_user



class AccessControlMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        if await check_user(user_id):

            return await handler(event, data)
        else:

            await event.answer("Sorry, you do not have access to this bot. Please contact support for assistance.")
            return
