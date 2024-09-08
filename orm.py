import sqlite3

class ORM:

    def __init__(self):

        self.sqlite_connection = sqlite3.connect('database.db')
        self.cursor = self.sqlite_connection.cursor()


    def __close_connection(self):

        self.cursor.close()
        self.sqlite_connection.close()


    def write_message_data(self, username: str, user_link: str, channel_name: str,
                           message_text: str, message_link: str, message_date: str,
                           is_reply: bool, replied_message_text: str, replied_message_link: str,
                           replied_username: str, replied_user_link: str):

        sqlite_select_query = """INSERT INTO messages (username, user_link, channel_name, message_text, message_link, message_date, is_reply, replied_message_text, replied_message_link, replied_username, replied_user_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(sqlite_select_query, (username, user_link, channel_name, message_text, message_link, message_date,
                                                  is_reply, replied_message_text, replied_message_link, replied_username, replied_user_link))
        self.sqlite_connection.commit()

        self.__close_connection()