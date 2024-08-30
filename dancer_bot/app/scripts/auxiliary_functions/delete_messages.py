async def delete_previous_messages_bot(bot, chat_id, user_id, latest_messages):
    if user_id in latest_messages:
        bot_message_id = latest_messages[user_id][0]
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            print(f"Error deleting message: {e}")


async def delete_previous_messages_user(bot, chat_id, user_id, latest_messages):
    if user_id in latest_messages:
        user_message_id = latest_messages[user_id][-1]
        try:
            await bot.delete_message(chat_id=chat_id, message_id=user_message_id)
        except Exception as e:
            print(f"Error deleting message: {e}")