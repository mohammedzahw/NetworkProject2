from socket import *
from threading import Thread
from tkinter import *


def submit(session, sender, reciever, msg, list_box):
    try:
        if msg.get() == "":
            return
        session.send(f"message,{sender},{reciever},{msg.get()}".encode("utf-8"))
        list_box.insert(END, f"{sender} >> {msg.get()}")
        list_box.yview(END)
        list_box.update_idletasks()
        # Insert the message # Scroll to the bottom
        msg.delete(0, END)
    except Exception as e:
        print("error9", e)


def submit_group(session, group_name, msg, list_box, sender):
    try:
        if msg.get() == "":
            return
        message = f"{sender} >> {msg.get()}"
        session.send(f"message group,{group_name},{message}".encode("utf-8"))
        # list_box.insert(
        #     END, f"{sender} >> {msg.get()}"
        # )  # Insert the message # Scroll to the bottom
        msg.delete(0, END)
    except Exception as e:
        print("error8", e)


def receive_message(session, list_box):
    while True:
        try:
            message = session.recv(2048).decode("utf-8")
            print("message", message)
            list_box.insert(END, message)
            list_box.yview(END)
            list_box.update_idletasks()

        except Exception as e:
            print("error6", e)
            break


def createchat(sender, reciever):
    print("createchat")
    global root
    try:
        print("seder", sender)
        print("reciever", reciever)
        if len(chat_sessions) > 0:
            for i in chat_sessions:
                i.close()
                chat_sessions.remove(i)
        session = socket(AF_INET, SOCK_STREAM)
        session.connect(("127.0.0.1", 8000))

        session.send(f"create chat,{sender},{reciever}".encode("utf-8"))
        print("create chat")
        Messages_str = session.recv(2048).decode("utf-8")
        Messages = Messages_str.split(",")[1:]
        print("Messages", Messages)
        if Messages == [""]:
            Messages = []
        Labels = Label(root, text=reciever, font="arial 15").place(
            x=230, y=0, width=150
        )
        list_box = Listbox(root, font="arial 12")
        list_box.place(x=210, y=30, width=180, height=320)
        for message in Messages:
            list_box.insert(END, message)
            list_box.yview(END)
            list_box.update_idletasks()
        Thread(
            target=receive_message,
            args=(
                session,
                list_box,
            ),
        ).start()
        msg = Entry(root, font="arial 10")
        msg.place(x=210, y=340, width=180, height=30)
        Button(
            root,
            text="send",
            font="arial 12",
            command=lambda session=session, sender=sender, receiver=reciever, msg=msg, list_box=list_box: submit(
                session, sender, receiver, msg, list_box
            ),
        ).place(x=210, y=370, width=180)
        chat_sessions.append(session)
    except Exception as e:
        print("error7", e)


def open_group_chat(sender, group_name):
    global root
    try:
        if len(chat_sessions) > 0:
            for i in chat_sessions:
                i.close()
                chat_sessions.remove(i)
        session = socket(AF_INET, SOCK_STREAM)
        session.connect(("127.0.0.1", 8000))
        chat_sessions.append(session)
        session.send(f"group messages,{group_name},{sender}".encode("utf-8"))
        print("group messages")
        Labels = Label(root, text=group_name, font="arial 15").place(
            x=230, y=0, width=150
        )
        Messages_str = session.recv(2048).decode("utf-8")
        Messages = Messages_str.split(",")[1:]
        if Messages == [""]:
            Messages = []
        print("Messages", Messages)
        list_box = Listbox(root, font="arial 12")
        list_box.place(x=210, y=30, width=180, height=320)
        for message in Messages:
            list_box.insert(END, message)
            list_box.yview(END)
            list_box.update_idletasks()
        Thread(
            target=receive_message,
            args=(
                session,
                list_box,
            ),
        ).start()
        msg = Entry(root, font="arial 10")
        msg.place(x=210, y=340, width=180, height=30)
        Button(
            root,
            text="send",
            font="arial 12",
            command=lambda: submit_group(session, group_name, msg, list_box, sender),
        ).place(x=210, y=370, width=180)
    except Exception as e:
        print("error1", e)


def save_group(group_name, user_name, fr):
    try:
        if group_name == "":
            return
        session = socket(AF_INET, SOCK_STREAM)
        session.connect(("127.0.0.1", 8000))
        session.send(f"create group,{group_name}".encode("utf-8"))
        fr.destroy()
        session.close()
        get_groups(user_name)
    except Exception as e:
        print("error2", e)


def create_group(user_name):
    try:

        fr = Frame(root, border=1, relief="solid", width=200, height=380)
        fr.place(x=10, y=10)
        Label(fr, text="Enter group name", font="arial 15").place(x=20, y=20)
        group_name = Entry(fr, font="arial 15")
        group_name.place(x=0, y=70, width=190, height=30)

        Button(
            fr,
            text="Create",
            font="arial 15",
            command=lambda: save_group(group_name.get(), user_name, fr),
        ).place(x=10, y=100, width=180, height=30)

    except Exception as e:
        print("error3", e)


def get_connected_users(user_name):
    try:
        session = socket(AF_INET, SOCK_STREAM)
        session.connect(("127.0.0.1", 8000))
        session.send(f"get users,{user_name}".encode("utf-8"))
        user_str = session.recv(2048).decode("utf-8")
        session.close()
        # session.close()
        users = user_str.split(",")[1:]
        if users == [""]:
            users = []
        # users=["Ahmed","Mohamed","Reda","Ahmed","Mohamed","Reda","Ahmed","Mohamed","Reda"]
        print("users", users)
        fr = Frame(root, border=1, relief="solid", width=200, height=380)
        fr.place(x=10, y=40)

        users = [user for user in users if user != user_name]

        # fr.destroy()
        for i, user in enumerate(users):
            print("user_name", user_name)
            print("user", user)
            Button(
                root,
                font="arial 12",
                text=user,
                command=lambda sender=user_name, receiver=user: createchat(
                    sender, receiver
                ),
            ).place(x=10, y=40 + i * 30, width=200, height=30)
    except Exception as e:
        print("error4", e)


def get_groups(user_name):
    try:
        session = socket(AF_INET, SOCK_STREAM)
        session.connect(("127.0.0.1", 8000))
        session.send(f"get groups,".encode("utf-8"))
        groups_str = session.recv(2048).decode("utf-8")
        session.close()
        groups = groups_str.split(",")[1:]
        if groups == [""]:
            groups = []
        # users=["Ahmed","Mohamed","Reda","Ahmed","Mohamed","Reda","Ahmed","Mohamed","Reda"]
        print("groups", groups)
        fr = Frame(root, border=1, relief="solid", width=200, height=380)
        fr.place(x=10, y=40)
        Button(
            root,
            font="arial 12",
            text="new group",
            command=lambda: create_group(user_name),
        ).place(x=10, y=40, width=200, height=30)

        # fr.destroy()
        for i, group in enumerate(groups):
            Button(
                root,
                font="arial 12",
                text=group,
                command=lambda sender=user_name, group_name=group: open_group_chat(
                    sender, group_name
                ),
            ).place(x=10, y=70 + i * 30, width=200, height=30)
    except Exception as e:
        print("error5", e)


def connect(user_name):
    try:
        login.destroy()
        root.title(f"{user_name}")
        client = socket(AF_INET, SOCK_STREAM)
        # print(f"{user_name}user_name")
        frame = Frame(root, border=1, relief="solid", width=200, height=380)
        frame.place(x=10, y=10)
        client.connect(("127.0.0.1", 8000))
        client.send(
            f"user_name,{user_name}".encode("utf-8")
        )  # client.send(user_name.encode('utf-8'))
        client.close()
        Button(
            root,
            text="users",
            font="arial 12",
            command=lambda: get_connected_users(user_name),
        ).place(x=110, y=10, width=100, height=30)
        Button(
            root,
            text="groups",
            font="arial 12",
            command=lambda: get_groups(user_name),
        ).place(x=10, y=10, width=100, height=30)
        root.update()
    except Exception as e:
        print("error10", e)


def on_closing():
    try:
        for i in chat_sessions:
           i.close()
        chat_sessions.clear()
        root.destroy()
    except Exception as e:
        root.destroy()
        print("error11", e)


root = Tk()
login = Frame(root, border=1, relief="solid", width=400, height=400)
root.geometry("400x400")
root.title("Chat")
root.protocol("WM_DELETE_WINDOW", on_closing)
list_box = Listbox(root)
chat_sessions = []


def main():

    Label(login, text="Enter your user_name", font="arial 15").place(x=100, y=100)
    login.pack()
    user_name = Entry(login, font="arial 15")
    user_name.place(x=50, y=150, width=300, height=50)
    Button(
        login, text="Enter", font="arial 15", command=lambda: connect(user_name.get())
    ).place(x=150, y=250, width=100, height=30)
    root.mainloop()


if __name__ == "__main__":
    main()


# Add buttons to the frame
