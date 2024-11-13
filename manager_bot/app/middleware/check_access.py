from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update
from app.database.requests.check_user import (
    check_user,
    check_user_have_chat_id_registered,
)


class AccessControlMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id

        if await check_user(user_id):
            await check_user_have_chat_id_registered(
                user_id, data["event_context"].chat.id
            )
            return await handler(event, data)
        else:
            await event.answer(
                "Sorry, you do not have access to this bot. Please contact support for assistance."
            )
            return
