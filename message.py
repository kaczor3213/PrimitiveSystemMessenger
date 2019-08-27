from datetime import datetime
from database import Database, DatabaseError

class Message:
    __id = -1
    from_id = -1
    to_id = -1
    text = ""
    creation_date = None
    title = ""

    def __init__(self):
        self.__id = -1
        self.from_id = -1
        self.to_id = -1
        self.text = ""
        self.creation_date = None
        self.title = ""

    def make_message(self, poster, receiver, message_content="Empty message", timestamp=datetime.now(), title="No title."):
        self.from_id = poster
        self.to_id = receiver
        self.title = title
        self.text = message_content
        self.creation_date = timestamp

    @staticmethod
    def __find_by_atr(cursor, atr, value):
        querry = None
        if atr == "id":
            querry = cursor.mogrify("SELECT * FROM messages WHERE id=%s;", (value,))
        elif atr == "from_id":
            querry = cursor.mogrify("SELECT * FROM messages WHERE from_id=%s;", (value,))
        elif atr == "to_id":
            querry = cursor.mogrify("SELECT * FROM messages WHERE to_id=%s;", (value,))
        cursor.execute(querry)
        return cursor.fetchone()

    def load_from_list(self, l):
        self.from_id = l[0]
        self.to_id = l[1]
        self.text = l[2]
        self.creation_date = l[3]
        self.title = l[4]

    def load_by_id(self, cursor, message_id):
        if self.__find_by_atr(cursor, "id", message_id) == None:
            print("There is no message with given id: %s",(message_id,))
        else:
            querry = cursor.mogrify("SELECT * FROM messages WHERE id=%s",(message_id,))
            cursor.execute(querry)
            l = cursor.fetchone()
            self.__id = l[0]
            self.from_id = l[1]
            self.to_id = l[2]
            self.text = l[3]
            self.creation_date = l[4]
            self.title = l[5]

    @staticmethod
    def load_all_messages(cursor, atr = None , value = None):
        if atr == value == None:
            querry = f"""SELECT * FROM messages;"""
            cursor.execute(querry)
            for record in cursor.fetchall():
                m = Message()
                m.__id = record[0]
                m.from_id = record[1]
                m.to_id = record[2]
                m.text = record[3]
                m.creation_date = record[4]
                m.title = record[5]
                yield m
        else:
            if __class__.__find_by_atr(cursor, atr, value) == None:
                print(f"Couldn't find any record applying to condition!")
                return False
            else:
                querry = cursor.mogrify("SELECT * FROM users WHERE %s LIKE(%s);",(atr, value))
                cursor.execute(querry)
                for record in cursor.fetchall():
                    m.__id = record[0]
                    m.from_id = record[1]
                    m.to_id = record[2]
                    m.text = record[3]
                    m.creation_date = record[4]
                    m.title = record[5]
                    yield m

    def save(self, cursor):
        querry = cursor.mogrify("INSERT INTO messages(from_id,to_id,text,creation_date,title) VALUES(%s, %s, %s, %s, %s);",(self.from_id, self.to_id, self.text, self.creation_date, self.title))
        cursor.execute(querry)
        return cursor.statusmessage != ""
    
    def __str__(self):
        s = f"""
            Message from: \t{self.from_id}
            \t\tto: \t{self.to_id}
            Posted at: \t{self.creation_date}
            Message:  \t#__{self.title}__#
            \t\t{self.text}
            """
        return s


if __name__ == '__main__':
    d = Database()
    d.configure_connection('postgres', 'dupa',database='messenger')
    d.connect()
    d.enable_cursor()
    #m = Message()
    #m.load_from_list([1,2,'Już cię więcej nie kocham seksistowska świnio!', datetime.now(), 'Nieudana miłość'])
    #print(m.save(d.cursor))
    for m in Message.load_all_messages(d.cursor):
        print(m)
