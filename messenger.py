from message import Message
from user import User
from database import Database
from getpass import getpass
from clcrypto import check_password
import argparse
import re

parser = argparse.ArgumentParser()

parser.add_argument('-u', '--user', action="store", help="Give a user mail, obligatory.")
parser.add_argument('-p', '--password', action="store", help="Giva a user password, obligatory.")
parser.add_argument('-n', '--new_password', action="store", help="Set a new password for given user")
parser.add_argument('-l', '--list', action="store_true", help="List all users in database.")
parser.add_argument('-d', '--delete', action="store_true", help="Delete a given user.")
parser.add_argument('-e', '--edit', action="store_true", help="Edit data for a given user.")
parser.add_help = True
args = parser.parse_args()

d = Database()
d.configure_connection('postgres', 'dupa', database='messenger')
d.connect()
d.enable_cursor()
u = User()


def start_shell():
    command = ""
    while (command != 'exit'):
        command = input(f"{u.username}@messenger$: ")
        if command == f"send_message":
            r = User()

            if r.load_by_email(d.cursor, input(f"{u.username}@messenger$: Podaj odbiorcę:\t")):
                t = input(f"{u.username}@messenger$: Podaj tytuł:\t")
                content = input(f"{u.username}@messenger$: Treść:\t")
                u.post_message(d.cursor, t, content, (r.id,))
                u.read_last_posted_message(d.cursor)

        elif command == f"read_message":
            u.read_last_received_message(d.cursor)

        else:
            print("SyntaxError")


if args.user != None and args.password != None:

    if u.load_by_email(d.cursor, args.user) and u.check_password(d.cursor, args.password):

        if args.edit == True:
            tmp0 = input(f"messenger$: Podaj nową nazwę użytkownika: (default={u.username})\t")
            if tmp0 == "":
                pass
            else:
                u.username = tmp0
            if u.update(d.cursor):
                print(
                    "Utworzyłeś nowe konto w aplikacji messenger, teraz zaloguj się na swoje konto korzystając z komendy: \n messenger -u email@email.com")
                exit()

        if args.new_password == True:
            t = True
            while (t):
                tmp1 = getpass("messenger$: Podaj nowe hasło:\t")
                tmp2 = getpass("messenger$: Powtórz swoje hasło:\t")
                if tmp1 == tmp2:
                    u.set_hashed_password(tmp1)
                    t = False
                else:
                    print("Podane hasła się nie pokrywają.")

        if args.delete == True and args.edit == False and args.new_password == False:
            if u.delete(d.cursor):
                print("Konto zostało usunięte z powodzeniem, żałujemy, że nie zostałeś z nami na dłużej.")
                exit()
            else:
                print("Próba usunięcia konta, zakończyła się niepowodzeniem, zostaniesz z nami dłużej, hehehehe...")
        elif args.delete == True:
            parser.print_help()
            exit()

        if args.list == True:
            for i in User.load_all(d.cursor):
                print(i)

        start_shell()

if args.user == None:
    parser.print_help()
else:
    if not u.load_by_email(d.cursor, args.user):
        print("#_____Witaj_w_aplikacji_messenger!_____#")
        u.username = input("messenger$: Podaj nazwę użytkownika:\t")
        u.email = input("messenger$: Podaj swój email:\t")
        t = True
        while (t):
            tmp1 = getpass("messenger$: Podaj swoje hasło:\t")
            tmp2 = getpass("messenger$: Powtórz swoje hasło:\t")
            if tmp1 == tmp2:
                u.set_hashed_password(tmp1)
                t = False
            else:
                print("Podane hasła się nie pokrywają.")
        if u.save(d.cursor):
            print(
                "Utworzyłeś nowe konto w aplikacji messenger, teraz zaloguj się na swoje konto korzystając z komendy: \n messenger -u email@email.com")
            exit()
        else:
            print("Próba utworzenia nowego konta, zakończyła się niepowodzeniem!")
            exit()
    else:
        if args.password != None and u.check_password(d.cursor, args.password):
            start_shell()
        else:
            if u.check_password(d.cursor, getpass("messenger$: Podaj swoje hasło:\t")):
                start_shell()
            else:
                print("Błędne hasło!")
                exit()

d.disconnect()
