from socket import *
from threading import Thread
import json

server = socket(AF_INET, SOCK_STREAM)
server.bind(("127.0.0.1", 8000))
server.listen(5)
print("Server is listening on port 8000")


# *****************************************************************



# *****************************************************************


class Group:
    def __init__(self, name):
        self.name = name
        self.messages = []
        self.sessions = {}

    def add_message(self, message):
        self.messages.append(message)

    def add_user(self, user):
        self.users.append(user)

    def add_session(self, user_name, session):
        self.sessions[user_name] = session

    def get_session(self, user_name):
        return self.sessions[user_name]


# *****************************************************************
class Chat:
    def __init__(self, name, sender, reciever):
        self.name = name
        self.messages = []
        self.sessions = {sender: None, reciever: None}

    def send(self, message):
        self.session.send(message)

    def add_message(self, message):
        self.messages.append(message)

    def add_session(self, user_name, session):
        self.sessions[user_name] = session

    def get_session(self, user_name):
        return self.sessions[user_name]


# *****************************************************************
users = {}
groups = []
chats = []


def recv(client):
    while True:
        try:
            msg = client.recv(2048)
            msgcontent = msg.decode("utf-8").split(",")
            print("msgcontent", msgcontent)
            if msgcontent==['']:
                break

            if msgcontent[0] == "create group":
                group = Group(msgcontent[1])
                groups.append(group)

            elif msgcontent[0] == "get groups":
                get_groups(client)
            elif msgcontent[0] == "group messages":
                groupname = msgcontent[1]
                sender = msgcontent[2]
                print("groupname", groupname)
                print("sender", sender)
                group = next(
                    (group for group in groups if group.name == groupname), None
                )
                group.add_session(sender, client)
                client.send(("messages," + ",".join(group.messages)).encode("utf-8"))

            elif msgcontent[0] == "message group":
                groupname = msgcontent[1]
                message = msgcontent[2]
                group = next(
                    (group for group in groups if group.name == groupname), None
                )
                for session in group.sessions.values():
                    try:
                        session.send(message.encode("utf-8"))
                    except Exception as e:
                        print("session closed", e) 
                  
                group.add_message(message)

            elif msgcontent[0] == "get users":
                get_connected_users(client)

            elif msgcontent[0] == "create chat":
                sender = msgcontent[1]
                receiver = msgcontent[2]
                chatname1 = sender + "-" + receiver
                chatname2 = receiver + "-" + sender
                chat = next(
                    (
                        chat
                        for chat in chats
                        if chat.name == chatname1 or chat.name == chatname2
                    ),
                    None,
                )
                if chat is None:
                    newchat = Chat(chatname1, sender, receiver)
                    newchat.add_session(sender, client)
                    chats.append(newchat)
                    print("chat created", newchat.name)
                    client.send(
                        ("messages," + ",".join(newchat.messages)).encode("utf-8")
                    )
                else:
                    chat.add_session(sender, client)
                    client.send(("messages," + ",".join(chat.messages)).encode("utf-8"))
                    print("chat", chat.name)

            elif msgcontent[0] == "message":
                sender = msgcontent[1]
                receiver = msgcontent[2]
                chatname1 = sender + "-" + receiver
                chatname2 = receiver + "-" + sender
                chat = next(
                    (
                        chat
                        for chat in chats
                        if chat.name == chatname1 or chat.name == chatname2
                    ),
                    None,
                )
                print("chat", chat)
                print("sender", chat.sessions[sender])
                print("receiver", chat.sessions[receiver])
                if chat.get_session(receiver) is not None:
                    try:
                        chat.sessions[receiver].send(
                            f"{sender} >> {msgcontent[3]}".encode("utf-8")
                        )
                    except:
                        print("session closed")
                chat.add_message(f"{sender} >> {msgcontent[3]}")
            elif msgcontent[0] == "user_name":
                name = msgcontent[1]
                users[name] = name
                get_connected_users(client)
        except Exception as e:
            print("error", e)
            break


def get_groups(client):
    groups_names = [group.name for group in groups]
    client.send(("groups,"+",".join(groups_names)).encode("utf-8"))


def get_connected_users(client):
    for user in users:
        users_names = [key for key in users]
        print("users", users)
        print("users_names", users_names)
        client.send(("users," + ",".join(users_names)).encode("utf-8"))

# *****************************************************************


while True:
    client, addr = server.accept()
    Thread(target=recv, args=(client,)).start()


server.close()
