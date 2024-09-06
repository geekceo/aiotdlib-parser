import asyncio
import logging

from aiotdlib import Client, ClientSettings
from aiotdlib.api import BaseObject, UpdateNewMessage, MessageLink
from aiotdlib.client import API

from datetime import datetime

from orm import ORM

API_ID = 25014319
API_HASH = '3813e6baf9ab9915b08b810e9bde7b5b'
PHONE_NUMBER = '79013375451'

chat_users_dict: dict = {}

async def on_update_new_message(client: Client, update: UpdateNewMessage):
    chat_id = update.message.chat_id

    # api field of client instance contains all TDLib functions, for example get_chat
    chat = await client.api.get_chat(chat_id)
    logging.info(f'Message received in chat {chat.title}')

    print(chat.id)

    #if chat_id not in chat_users_dict.keys:

    #    chat_users_dict[chat_id] = chat.chat_lists

    user_data = await client.api.get_user(user_id=update.message.sender_id.user_id)

    user_first_last_names: str = f"{user_data.first_name} {user_data.last_name}"

    chat_id: str = str(chat.id).replace('-1001', '')

    channel_name: str = chat.title

    message_link: str = await client.api.get_message_link(chat_id=chat.id, message_id=update.message.id) #f'https://t.me/c/{chat_id}/{update.message.id}'

    message_date: str = datetime.fromtimestamp(update.message.date).strftime('%d-%m-%Y %H:%M:%S')

    message_text: str = '-'
    username: str = '-'
    user_link: str = '-'

    

    try:

        message_text = update.message.content.text.text

        try:

            username = user_data.usernames.editable_username
            user_link = f"https://t.me/{user_data.usernames.editable_username}"

        except AttributeError:

            username = user_first_last_names

        #logging.info(f'{update.message.sender_id.user_id}: {update.message.content.text.text}')

        ORM().write_message_data(username=username, user_link=user_link, channel_name=channel_name,
                           message_text=message_text, message_link=message_link.link, message_date=message_date)

    except AttributeError:

        ...




#async def any_event_handler(client: Client, update: BaseObject):
#    logging.info(f'Event of type {update.ID} received')


async def main():
    client = Client(
        settings=ClientSettings(
            api_id=API_ID,
            api_hash=API_HASH,
            phone_number=PHONE_NUMBER
        )
    )

    # Registering event handler for 'updateNewMessage' event
    # You can register many handlers for certain event type
    client.add_event_handler(on_update_new_message, update_type=API.Types.UPDATE_NEW_MESSAGE)

    # You can register handler for special event type "*". 
    # It will be called for each received event
    #client.add_event_handler(any_event_handler, update_type=API.Types.ANY)

    async with client:
        # idle() will run client until it's stopped
        await client.idle()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())