from socket import *
from threading import Thread
from tkinter import *


def submit(session, sender, reciever, msg, list_box):
    print(type(session))
    if msg.get() == "":
        return
    session.send(f"message,{sender},{reciever},{msg.get()}".encode("utf-8"))
    list_box.insert(
        END, f"{sender} >> {msg.get()}"
    )  # Insert the message # Scroll to the bottom
    msg.delete(0, END)


def submit_group(session, name, msg, list_box, sender):
    print(type(session))
    if msg.get() == "":
        return
    message=f"{sender} >> {msg.get()}"
    session.send(f"message group,{name},{message}".encode("utf-8"))
    # list_box.insert(
    #     END, f"{sender} >> {msg.get()}"
    # )  # Insert the message # Scroll to the bottom
    msg.delete(0, END)


def receive_message(session, list_box):
    while True:
        try:
            message = session.recv(2048).decode("utf-8")
            print("message", message)
            list_box.insert(END, message)
            list_box.update_idletasks()

        except Exception as e:
            print("error", e)
            break


def createchat(sender, reciever):
    global Message
    global root
    if len(chat_sessions) > 0:
        for i in chat_sessions:
            i.close()
            chat_sessions.remove(i)
    session = socket(AF_INET, SOCK_STREAM)
    session.connect(("127.0.0.1", 8000))
    chat_sessions.append(session)
    session.send(f"create chat,{sender},{reciever}".encode("utf-8"))
    Messages_str = session.recv(2048).decode("utf-8")
    Messages = Messages_str.split(",")[1:]
    print("Messages", Messages)

    list_box = Listbox(root, font="arial 12")
    list_box.place(x=350, y=0, width=400, height=700)
    for message in Messages:
        list_box.insert(END, message)
        list_box.update_idletasks()
    Thread(
        target=receive_message,
        args=(
            session,
            list_box,
        ),
    ).start()
    msg = Entry(root, font="arial 10")
    msg.place(x=350, y=720, width=400, height=30)
    Button(
        root,
        text="send",
        font="arial 12",
        command=lambda session=session, sender=sender, receiver=reciever, msg=msg, list_box=list_box: submit(
            session, sender, receiver, msg, list_box
        ),
    ).place(x=350, y=750, width=400)


def open_group_chat(sender, name):
    global root
    try:
        if len(chat_sessions) > 0:
            for i in chat_sessions:
                i.close()
                chat_sessions.remove(i)
        session = socket(AF_INET, SOCK_STREAM)
        session.connect(("127.0.0.1", 8000))
        chat_sessions.append(session)
        session.send(f"group messages,{name},{sender}".encode("utf-8"))
        print("group messages")
        Messages_str = session.recv(2048).decode("utf-8")
        Messages = Messages_str.split(",")[1:]
        print("Messages", Messages)
        list_box = Listbox(root, font="arial 12")
        list_box.place(x=350, y=0, width=400, height=700)
        for message in Messages:
            list_box.insert(END, message)
            list_box.update_idletasks()
        Thread(
            target=receive_message,
            args=(
                session,
                list_box,
            ),
        ).start()
        msg = Entry(root, font="arial 10")
        msg.place(x=350, y=720, width=400, height=30)
        Button(
            root,
            text="send",
            font="arial 12",
            command=lambda session=session, name=name, msg=msg, list_box=list_box, sender=sender: submit_group(
                session, name, msg, list_box, sender
            ),
        ).place(x=350, y=750, width=400)
    except Exception as e:
        print("error", e)

def save_group(name,fr):
    try:
        session = socket(AF_INET, SOCK_STREAM)
        session.connect(("127.0.0.1", 8000))
        session.send(f"create group,{name}".encode("utf-8"))
        fr.destroy()
        get_groups(name)
        session.close()
    except Exception as e:
        print("error", e)
def create_group():
    try:
       
        fr=Frame(root, border=1, relief="solid", width=300, height=750)
        fr.place(x=10, y=10)
        Label(fr, text="Enter group name", font="arial 15").place(x=50, y=20)
        name = Entry(fr, font="arial 15")
        name.place(x=10, y=70, width=280, height=50)
    
        Button(
            fr, text="Create", font="arial 15", command=lambda: save_group(name.get(),fr)
        ).place(x=10, y=150, width=280, height=30)
        
        
    except Exception as e:
        print("error", e)


def get_connected_users(name):
    try:
        session = socket(AF_INET, SOCK_STREAM)
        session.connect(("127.0.0.1", 8000))
        session.send(f"get users,{name}".encode("utf-8"))
        user_str = session.recv(2048).decode("utf-8")
        session.close()
        # session.close()
        users = user_str.split(",")[1:]
        if users==['']:
            users=[]
        # users=["Ahmed","Mohamed","Reda","Ahmed","Mohamed","Reda","Ahmed","Mohamed","Reda"]
        print("users", users)
        fr = Frame(root, border=1, relief="solid", width=300, height=750)
        fr.place(x=10, y=50)

        users = [user for user in users if user != name]

        # fr.destroy()
        for i, user in enumerate(users):
            Button(
                root,
                font="arial 12",
                text=user,
                command=lambda reciever=user, sender=name: createchat(sender, reciever),
            ).place(x=10, y=50 + i * 40, width=300, height=40)
    except Exception as e:
        print("error", e)


def get_groups(name):
    try:
        session = socket(AF_INET, SOCK_STREAM)
        session.connect(("127.0.0.1", 8000))
        session.send(f"get groups,".encode("utf-8"))
        groups_str = session.recv(2048).decode("utf-8")
        session.close()
        groups = groups_str.split(",")[1:]
        if groups==['']:
            groups=[]
        # users=["Ahmed","Mohamed","Reda","Ahmed","Mohamed","Reda","Ahmed","Mohamed","Reda"]
        print("groups", groups)
        fr = Frame(root, border=1, relief="solid", width=300, height=750)
        fr.place(x=10, y=100)
        Button(
                root,
                font="arial 12",
                text="new group",
                command=lambda: create_group(),
            ).place(x=10, y=50, width=300, height=40)

        # fr.destroy()
        for i, group in enumerate(groups):
            Button(
                root,
                font="arial 12",
                text=group,
                command=lambda: open_group_chat(name, group),
            ).place(x=10, y=100 + i * 40, width=300, height=40)
    except Exception as e:
        print("error", e)


def connect(name):
    login.destroy()
    root.title(f"{name}")
    client = socket(AF_INET, SOCK_STREAM)
    # print(f"{name}name")
    frame = Frame(root, border=1, relief="solid", width=300, height=700)
    frame.place(x=10, y=50)
    client.connect(("127.0.0.1", 8000))
    client.send(f"name,{name}".encode("utf-8"))  # client.send(name.encode('utf-8'))
    client.close()
    Button(
        root,
        text="users",
        font="arial 12",
        command=lambda name=name, client=client: get_connected_users(name),
    ).place(x=160, y=10, width=150, height=30)
    Button(
        root,
        text="groups",
        font="arial 12",
        command=lambda name=name, client=client: get_groups(name),
    ).place(x=10, y=10, width=150, height=30)
    root.update()


root = Tk()
login = Frame(root, border=1, relief="solid", width=400, height=600)
root.geometry("800x800")
root.title("Chat")
list_box = Listbox(root)
chat_sessions = []


def main():

    Label(login, text="Enter your name", font="arial 15").place(x=100, y=150)
    login.pack()
    name = Entry(login, font="arial 15")
    name.place(x=50, y=200, width=300, height=50)
    Button(
        login, text="Enter", font="arial 15", command=lambda: connect(name.get())
    ).place(x=150, y=250, width=100, height=30)
    root.mainloop()


if __name__ == "__main__":
    main()


# Add buttons to the frame
