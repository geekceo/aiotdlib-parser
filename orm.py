import sqlite3

class ORM:

    def __init__(self):

        self.sqlite_connection = sqlite3.connect('database.db')
        self.cursor = self.sqlite_connection.cursor()


    def __close_connection(self):

        self.cursor.close()
        self.sqlite_connection.close()


    def write_message_data(self, username: str, user_link: str, channel_name: str,
                           message_text: str, message_link: str, message_date):

        sqlite_select_query = """INSERT INTO messages (username, user_link, channel_name, message_text, message_link, message_date) VALUES (?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(sqlite_select_query, (username, user_link, channel_name, message_text, message_link, message_date))
        self.sqlite_connection.commit()

        self.__close_connection()