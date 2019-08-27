from database import Database, DatabaseError
from clcrypto import *
from message import Message
from datetime import datetime
import re

class User:
    __id = None
    username = None
    _email = None
    __hashed_password = None

    def __init__(self):
        self.__id = -1
        self.username = ""
        self._email = ""
        self.__hashed_password = None

    @property
    def id(self):
        if self.__id == -1:
            return f"This user doesn't exist in messenger_db!\nCode: {self.__id}"
        else:
            return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, user_email):
        self._email = user_email.lower()

    def __check_password_condition(self, cursor):
        if self.__id == -1:
            print("To get password salt, you have to load user first!")
            return False
        else:
            True

    def set_hashed_password(self, password, key=generate_salt()):
        if password == None or password == "":
            raise ValueError("Can't set an empty password!")
        self.__hashed_password = password_hash(password, key)

    def check_password(self, cursor, password):
        if self.__check_password_condition:
            querry = cursor.mogrify("SELECT hashed_password FROM users WHERE id=%s;", (self.__id,))
            cursor.execute(querry)
            h_pass = cursor.fetchone()[0]
            return check_password(password, h_pass)
        return False

    @staticmethod
    def __find_by_atr(cursor, atr, value):
        querry = None
        if atr == "id":
            querry = cursor.mogrify("SELECT * FROM users WHERE id=%s;", (value,))
        elif atr == "email":
            querry = cursor.mogrify("SELECT * FROM users WHERE email=%s;", (value,))
        cursor.execute(querry)
        return cursor.fetchone()

    def __condition_username(self):
        if self.username == "":
            raise ValueError("Username is not set!")
            
    def __condition_email(self, cursor):
        email_check_regex = r"""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
        if self.__find_by_atr(cursor,"email",self._email) != None:
            raise DatabaseError("Record with this email already exists!")
        elif re.search(email_check_regex,self._email) == None:
            print(re.search(email_check_regex,self._email))
            raise ValueError("Given email isn't valid!")

    def __condition_password(self):
        if self.__hashed_password == None:
            raise ValueError("Password is not set!")

    def __validate_username(self):
        try:
            self.__condition_username()
        except ValueError as e:
            print(e)
            t = input("Do you want to set your username to 'null'? (y/n):")
            if t.lower() == 'y':
                self.username = 'null'
                return True
            else:
                return False
        else:
            return True

    def __validate_email(self, cursor):
        try:
            self.__condition_email(cursor)
        except DatabaseError as e:
            print(e)
            return False
        except ValueError as e:
            print(e)
            return False
        else:
            return True

    def __validate_password(self):
        try:
            self.__condition_password()
        except ValueError as e:
            print(e)
            t = input("Do you want to generate random password? (y/n):")
            if t.lower() == 'y':
                self.set_hashed_password(generate_salt())
            else:
                return False
        else:
            return True

    def save(self, cursor):
        state = self.__validate_username() and self.__validate_email(cursor) and self.__validate_password()
        if state: 
            querry = cursor.mogrify("INSERT INTO users(username,email,hashed_password) VALUES(%s,%s,%s);",(self.username, self._email, self.__hashed_password))
            cursor.execute(querry)
            return state and (cursor.statusmessage != "")

    def update(self, cursor):
        if self.__id == -1:
            print("To get password salt, you have to load user first!")
            return False
        else:
            state = self.__validate_username() and self.__validate_email(cursor) and self.__validate_password()
            if state:
                querry = cursor.mogrify("UPDATE users SET username=%s, email=%s, hashed_password=%s WHERE id=%s;",(self.username, self._email, self.__hashed_password, user_id))
                cursor.execute(querry)
                return state and (cursor.statusmessage != "")
    
    def delete(self, cursor):
        if self.__id == -1:
            print("To get password salt, you have to load user first!")
            return False
        else:
            querry = cursor.mogrify("DELETE FROM users WHERE id=%s;",(self.__id,))
            cursor.execute(querry)
            return cursor.statusmessage != ""

    @staticmethod
    def delete_user(cursor, user_id):
        if __class__.__find_by_atr(cursor, "id", user_id) == None:
            print(f"There is no user with id: {user_id}")
            return False
        else:
            querry = cursor.mogrify("DELETE FROM users WHERE id=%s;",(user_id,))
            cursor.execute(querry)
            return cursor.statusmessage != ""
    
    def load_from_list(self, l):
        self.username = l[0]
        self._email = l[1]
        self.set_hashed_password(l[2])

    def load_by_id(self, cursor, user_id):
        if __class__.__find_by_atr(cursor, "id", user_id) == None:
            print(f"There is no user with id: {user_id}")
            return False
        else:
            querry = f"""SELECT * FROM users WHERE id={user_id};"""
            cursor.execute(querry)
            l = cursor.fetchone()
            self.__id = l[0]
            self.username = l[2]
            self._email = l[1]
            self.__hashed_password = l[3]
            return True
    
    def load_by_email(self, cursor, user_email):
        if __class__.__find_by_atr(cursor, "email", user_email) == None:
            print(f"There is no user with email: {user_email}")
            return False
        else:
            querry = cursor.mogrify("SELECT * FROM users WHERE email=%s;",(user_email,))
            cursor.execute(querry)
            l = cursor.fetchone()
            self.__id = l[0]
            self.username = l[2]
            self._email = l[1]
            self.__hashed_password = l[3]
            return True
    
    @staticmethod
    def load_all(cursor, atr = None , value = None):
        if atr == value == None:
            querry = f"""SELECT * FROM users;"""
            cursor.execute(querry)
            for record in cursor.fetchall():
                print(record)
                u = User()
                u.__id = record[0]
                u.username = record[2]
                u._email = record[1]
                u.__hashed_password = record[3]
                yield u
        else:
            if __class__.__find_by_atr(cursor, atr, value) == None:
                print(f"Couldn't find any record applying to condition!")
                return False
            else:
                querry = f"""SELECT * FROM users WHERE {atr} LIKE({value});"""
                cursor.execute(querry)
                for record in cursor.fetchall():
                    u = User()
                    u.__id = record[0]
                    u.username = record[1]
                    u._email = record[2]
                    u.__hashed_password = record[3]
                    yield u

    @staticmethod
    def broadcast_message(self, cursor):
        pass

    def post_message(self, cursor, title, message_content, receivers_id):
        if self.__id == -1:
            print("Can't post messages from not existing user!")
            return False
        else:
            for i in receivers_id:
                if self.__find_by_atr(cursor, "id", i) == "":
                    print("Can't post messages to not existing user!")
                    return False
                else:
                    m = Message()
                    m.make_message(self.__id,receivers_id, message_content, datetime.now(), title)
                    print(m)
                    return m.save(cursor)

    def read_all_received_messages(self, cursor):
        querry = f"""SELECT * FROM messages WHERE to_id={self.__id};"""
        cursor.execute(querry)
        m = Message()
        for record in cursor.fetchall():
            m.load_from_list(record)
            print(m)

    def read_all_posted_messages(self, cursor):
        querry = f"""SELECT * FROM messages WHERE from_id={self.__id};"""
        cursor.execute(querry)
        m = Message()
        if cursor.fetchone() == None:
            print("There aren't any messages received!")
        else:
            m.load_from_list(cursor.fetchone())
            print(m)
        for record in cursor.fetchall():
            m.load_from_list(record)
            print(m)

    def read_last_received_message(self, cursor):
        querry = f"""SELECT * FROM messages WHERE to_id={self.__id} ORDER BY creation_date DESC LIMIT 1;"""
        cursor.execute(querry)
        m = Message()
        if cursor.fetchone() == None:
            print("There aren't any messages received!")
        else:
            m.load_from_list(cursor.fetchone())
            print(m)

    def read_last_posted_message(self, cursor):
        querry = f"""SELECT * FROM messages WHERE to_id={self.__id} ORDER BY creation_date DESC LIMIT 1;"""
        cursor.execute(querry)
        m = Message()
        if cursor.fetchone() == None:
            print("There aren't any messages received!")
        else:
            m.load_from_list(cursor.fetchone())
            print(m)

    def __str__(self):
        return f"Id:\t{self.__id}\nUser:\t{self.username}\nEmail:\t{self.email}\nPass:\t{self.__hashed_password}\n"


if __name__ == '__main__':
    d = Database()
    d.configure_connection('postgres', 'dupa',database='messenger')
    d.connect()
    d.enable_cursor()
    marian = ('Marian', 'marian.pazdzioch@onet.pl', 'trudnehaslo')
    tytus = ('Tytus', 'kapitan.bomba@gwiezdnaflota.kurwix', 'petardatepychuj')
    ponury = ('Ponury', 'mroczny.zniwiarz@hades.com', 'billandmandy98')
    test1 = ('', '', '')
    test2 = ('', '', 'd')
    test3 = ('', 'anonim@anonim.anonim', 'd')
    test4 = ('JużNieAnonim', 'szach@mat.ateisci', 'dupa')
    test5 = ('DoWyjebki', 'wyjeb@mnie.thx', 'chujwie')
    #save test passed
    #update test passed
    #delete test passed
    #load_by_id test passed
    #load_by_email test passed
    #load_all test passed


    u = User()
    u.load_by_id(d.cursor,2)
    print(u)
    u.post_message(d.cursor,"Mam Cię w dupie!","Zignorowałeś mnie fiucie!, więcej się do Ciebie nie odzywam",(3,))
