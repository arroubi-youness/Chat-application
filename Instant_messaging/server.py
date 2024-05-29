import socket
import threading
import json
import sqlite3
import time

host = socket.gethostbyname(socket.gethostname())
port = 55580
ENCODER = 'utf-8'
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()
clients = []
nickname = []
rooms = {}
global client


def broadcast(message):
    for homme in clients:
        homme.send(message.encode(ENCODER))


def room_broadcast(messages, list_inside_room):
    for person in list_inside_room:
        person.send(messages.encode(ENCODER))


def create_table():
    database = sqlite3.connect("data.db")
    cursor = database.cursor()
    cursor.execute("""
               CREATE TABLE IF NOT EXISTS client(
               username TEXT,
               email TEXT,
               password TEXT)""")
    database.commit()
    database.close()


def create_message_priv():
    database = sqlite3.connect("data.db")
    cursor = database.cursor()
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS messagespriv (
      emetteur TEXT,
      mesage TEXT,
      reciever TEXT)""")
    database.commit()
    database.close()


def all_client():
    database = sqlite3.connect("data.db")
    cursor = database.cursor()
    cursor.execute('''SELECT username FROM client''')
    return cursor.fetchall()


def create_message_pub():
    try:
        with sqlite3.connect("data.db") as database:
            cursor = database.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messagespub (
                emetteur TEXT,
                mesage TEXT
                 )""")
    except sqlite3.Error as e:
        print(f"Error creating 'messages' table: {e}")


def histor_broadcast():
    database = sqlite3.connect("data.db")
    cursor = database.cursor()
    cursor.execute("SELECT emetteur,mesage FROM messagespub")
    return cursor.fetchall()


def priv_history_message(list_donnes):
    database = sqlite3.connect("data.db")
    cursor = database.cursor()

    cursor.execute("""
        SELECT emetteur, mesage 
        FROM messagespriv 
        WHERE (emetteur = ? AND reciever = ?) OR (emetteur = ? AND reciever = ?)
    """, (list_donnes[0], list_donnes[1], list_donnes[1], list_donnes[0]))
    return cursor.fetchall()


def insert_message_priv(history_list):
    database = sqlite3.connect("data.db")
    cursor = database.cursor()
    cursor.execute("INSERT INTO messagespriv VALUES(?,?,?)", (history_list[0], history_list[1], history_list[2]))
    database.commit()
    database.close()


def insert_message_pub(history_list):
    database = sqlite3.connect("data.db")
    cursor = database.cursor()
    cursor.execute("INSERT INTO messagespub VALUES(?,?)", (history_list[0], history_list[1]))
    database.commit()
    database.close()


def change_name(new_name):
    print(new_name)
    database = sqlite3.connect("data.db")
    cursor = database.cursor()
    cursor.execute('''  
            UPDATE client
            SET username =?
            WHERE username =?;
            ''', (new_name[1], new_name[0]))
    database.commit()
    database.close()


# def base_login(listt):
#  database = sqlite3.connect("data.db")
# cursor = database.cursor()

# cursor.execute('SELECT password FROM client WHERE username =?', (listt[0],))
# result = cursor.fetchall()
# print(result[2][0])


# if listt[2] == result[2][0]:
#  client.send("succes".encode("utf-8"))
# else:
#   client.send("error!".encode("utf-8"))


#   database.close()

def login_info(listati):
    print(listati)
    database = sqlite3.connect("data.db")
    cursor = database.cursor()

    cursor.execute("SELECT * FROM client WHERE username=? AND password=?", (listati[0], listati[1]))
    retenu = cursor.fetchone()
    print(retenu)
    database.close()
    return retenu is not None


def base_sign(listati):
    database = sqlite3.connect("data.db")
    cursor = database.cursor()
    try:
        cursor.execute('SELECT username FROM client WHERE username=?', (listati[0],))
        result = cursor.fetchone()
        if result:
            client.send("er".encode("utf-8"))
            print("dkhel")
        else:
            print("asf")
            client.send("good".encode("utf-8"))
            cursor.execute('INSERT INTO client VALUES(?, ?, ?)', (listati[0], listati[1], listati[2]))
            database.commit()

    except:
        print("error")


def add_room(room_id, participants):
    if room_id not in rooms:
        rooms[room_id] = participants


def send_message_to_room(room_id, message):
    if room_id in rooms:
        room_participants = rooms[room_id]
        for participant in room_participants:
            participant.send(message.encode("utf-8"))


def handle_function(client):
    global room_list
    global room_nom
    global namesss_addr
    while True:
        try:
            message = client.recv(1024).decode(ENCODER)
            print(message)

            if '#' in message:
                parts = message.split('#')
                alias = parts[1]
                alias = alias.strip()

                print("1")
                index = nickname.index(alias)
                clients[index].send(parts[0].encode(ENCODER))
                var = parts[0].split(":")

                listr = [var[0], var[1], alias]
                insert_message_priv(listr)

            elif message == "l":
                print("TRue")
                login_donne = client.recv(1024).decode("utf-8")
                jsn_log = json.loads(login_donne)
                verfiy = login_info(jsn_log)
                print(verfiy)
                if verfiy:
                    client.send("succes".encode("utf-8"))
                    nickname.append(jsn_log[0])
                else:
                    client.send("errororor".encode("utf-8"))

                print(nickname)

            elif message == "history":
                client.send("historic".encode("utf-8"))
                messagees = histor_broadcast()
                jsn_msg = json.dumps(messagees)
                client.send(jsn_msg.encode("utf-8"))
                print(messagees)

            elif message == "bdel":

                jsn_nom = client.recv(1024).decode("utf-8")
                names = json.loads(jsn_nom)
                client.send("avec succes".encode("utf-8"))
                print(names)
                change_name(names)
                broadcast(f" !!! {names[0]} changed his name to {names[1]} !!!")
                index = nickname.index(names[0])
                nickname[index] = names[1]




            elif message == "mconcti":
                all_clien = all_client()
                print(all_clien)
                json_dato = json.dumps(nickname)
                json_all_clien = json.dumps(all_clien)
                client.send("zzzz".encode("utf-8"))
                time.sleep(0.1)
                client.send(json_dato.encode("utf-8"))
                time.sleep(0.1)

                client.send(json_all_clien.encode("utf-8"))

                print("ffffffffffff")

            elif message == "seds":
                signupdata = client.recv(1024).decode("utf-8")
                jsn_sign = json.loads(signupdata)
                base_sign(jsn_sign)

            elif message == "hisprv":
                lis_n = client.recv(1024).decode("utf-8")
                names_prive = json.loads(lis_n)
                client.send("historicprv".encode("utf-8"))
                messagees_prv = priv_history_message(names_prive)
                jsn_msg_prv = json.dumps(messagees_prv)
                client.send(jsn_msg_prv.encode("utf-8"))
                print(messagees_prv)

            elif message == "r":
                room_nom = client.recv(1024).decode("utf-8")

                client.send("nnnnn".encode("utf-8"))
                time.sleep(0.1)
                jsn_room = json.dumps(nickname)
                client.send(jsn_room.encode("utf-8"))
            elif message == "--":

                participant = client.recv(1024).decode("utf-8")
                room_list = json.loads(participant)
                broadcast(f"room named {room_nom} has been created\n")
                namesss_addr = []
                print(room_list)
                for i in room_list:
                    if i in nickname:
                        index = nickname.index(i)
                        namesss_addr.append(clients[index])
                print('khrejt')
                add_room(room_nom, namesss_addr)
                room_broadcast("butt", namesss_addr)
                time.sleep(0.1)
                room_broadcast(room_nom, namesss_addr)


            elif "@" in message:
                room_lista = message.split("@")
                send_message_to_room(room_lista[1], room_lista[0])



            else:
                message = message.split(":")
                if len(message) == 2:
                    insert_message_pub(message)
                    broadcast(f"{message[0]}:{message[1]}")




        except Exception as e:
            print(f"Error in handle_function: {str(e)}")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            if index < len(nickname):
                alias = nickname[index]
                broadcast(f"Client named {alias} has left the room!\n")
                nickname.remove(alias)
            break


def recieving():
    global client
    while True:
        print("serveur is listen now")
        client, adress = server_socket.accept()
        clients.append(client)
        print(clients[0])
        thread = threading.Thread(target=handle_function, args=(client,))
        thread.start()


recieving()
