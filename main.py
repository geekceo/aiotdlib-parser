import asyncio
import logging

from aiotdlib import Client, ClientSettings
from aiotdlib.api import BaseObject, UpdateNewMessage, MessageLink, Message, MessageSender, MessageSenderUser, User, MessageText
from aiotdlib.client import API

from datetime import datetime

from orm import ORM
from api import API as DB_API

API_ID = 25014319
API_HASH = '3813e6baf9ab9915b08b810e9bde7b5b'
PHONE_NUMBER = '79013375451'

chat_users_dict: dict = {}

async def on_update_new_message(client: Client, update: UpdateNewMessage):
    chat_id = update.message.chat_id

    chat = await client.api.get_chat(chat_id)
    replied_message_id: int
    replied_message: Message
    replied_user_type: MessageSender
    replied_user: User
    is_reply = 0
    replied_username = '-'
    replied_user_link = '-'
    replied_message_link: MessageLink | str = '-'
    replied_message_text = '-'

    user_data = await client.api.get_user(user_id=update.message.sender_id.user_id)

    user_first_last_names: str = f"{user_data.first_name} {user_data.last_name}"

    chat_id: str = str(chat.id).replace('-1001', '')

    channel_name: str = chat.title

    message_link: MessageLink = await client.api.get_message_link(chat_id=chat.id, message_id=update.message.id) #f'https://t.me/c/{chat_id}/{update.message.id}'

    message_date: str = datetime.fromtimestamp(update.message.date).strftime('%d-%m-%Y %H:%M:%S')

    message_text: str = '-'
    username: str = '-'
    user_link: str = '-'

    

    try:

        message_text = update.message.content.text.text

        if update.message.reply_to != None:

            try:

                replied_message_id = update.message.reply_to.message_id
                replied_message = await client.api.get_message(chat_id=chat.id, message_id=replied_message_id)

                replied_user_type = replied_message.sender_id
                if isinstance(replied_user_type, MessageSenderUser):
                    replied_user = await client.api.get_user(user_id=replied_user_type.user_id)

                    if isinstance(replied_message.content, MessageText):

                        replied_message_text = replied_message.content.text.text
                        replied_message_link = await client.api.get_message_link(chat_id=chat.id, message_id=replied_message_id)
                        replied_message_link = replied_message_link.link

                    else:

                        raise ValueError('Message content is not text')

                    print('OK')
                    print(replied_message_text)

                    try:

                        replied_username = replied_user.usernames.editable_username
                        replied_user_link = f"https://t.me/{replied_username}"

                    except AttributeError:

                        replied_username = f'{replied_user.first_name} {replied_user.last_name}'

                    is_reply = 1
            except Exception as e:

                print(f'#### REPLY ERROR {e}')

        try:

            username = user_data.usernames.editable_username
            user_link = f"https://t.me/{username}"

        except AttributeError:

            username = user_first_last_names

        #logging.info(f'{update.message.sender_id.user_id}: {update.message.content.text.text}')

        #ORM().write_message_data(username=username, user_link=user_link, channel_name=channel_name,
        #                   message_text=message_text, message_link=message_link.link, message_date=message_date,
        #                   is_reply=is_reply, replied_message_text=replied_message_text, replied_message_link=replied_message_link,
        #                   replied_username=replied_username, replied_user_link=replied_user_link)

        DB_API().send_data(table_name=PHONE_NUMBER, username=username, user_link=user_link, channel_name=channel_name,
                           message_text=message_text, message_link=message_link.link, message_date=message_date,
                           is_reply=is_reply, replied_message_text=replied_message_text, replied_message_link=replied_message_link,
                           replied_username=replied_username, replied_user_link=replied_user_link)
        
        is_reply = 0

    except AttributeError as e:

        print(f'#### ERROR {e}')
        print(replied_message_text)




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