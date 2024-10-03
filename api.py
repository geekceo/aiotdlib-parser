import requests

class API:

    def __init__(self) -> None:
        
        self.api_route = 'http://185.117.154.136/set'

    def send_data(self, table_name: str, username: str, user_link: str, channel_name: str,
                    message_text: str, message_link: str, message_date: str,
                    is_reply: int, replied_message_text: str, replied_message_link: str,
                    replied_username: str, replied_user_link: str) -> None:

        headers = {
            'Content-type': 'application/json; charset=utf-8'
            }
        
        body_data = {
            'table_name': table_name,
            'username': username,
            'user_link': user_link,
            'channel_name': channel_name,
            'message_text': message_text,
            'message_link': message_link,
            'message_date': message_date,
            'is_reply': is_reply,
            'replied_message_text': replied_message_text,
            'replied_message_link' :replied_message_link,
            'replied_username': replied_username,
            'replied_user_link': replied_user_link
        }

        requests.post(
            url=self.api_route,
            json=body_data,
            headers=headers
        )