import socket
import tkinter.scrolledtext
import threading
from tkinter import *
from PIL import ImageTk, Image
import json
import time
from tkinter import messagebox

HOST = socket.gethostbyname(socket.gethostname())
PORT = 55580

sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_client.connect((HOST, PORT))
global frame_salon
global mesgehistory
global show_lista
global chngename
global create_room
global public_butt
global prive_butt
global nom
global new_namess
global scrollable_frame_crate
global rom_name
message_room = {}


def add_message(id_room, message):
    if id_room not in message_room:
        message_room[id_room] = message
        print(message_room[id_room])


def loginpage():
    def hide():
        pass_enter.config(show="*")
        eyeopbutt.config(command=show, image=eyeclose)

    def show():
        pass_enter.config(show="")
        eyeopbutt.config(command=hide, image=eyeop)

    def vider(event):
        if username_entery.get() == "Username":
            username_entery.delete(0, END)

    def viderpass(event):
        if pass_enter.get() == "Password":
            pass_enter.delete(0, END)

    def login():
        global nom
        nom = username_entery.get()
        password = pass_enter.get()
        nom = nom.strip()
        password = password.strip()
        if nom == '' and password == '':
            messagebox.showerror("ERROR!", "enter all data")

        loginlist = [nom, password]
        jsonlogin = json.dumps(loginlist)
        sock_client.send("l".encode("utf-8"))
        time.sleep(0.1)
        sock_client.send(jsonlogin.encode("utf-8"))
        reponse = sock_client.recv(1024).decode("utf-8")
        if reponse == "succes":
            print("hhhhhhhhhhhhhh")
            gui.destroy()
            gui_loop()
        elif reponse == "errororor":
            messagebox.showerror("ERROR!", "password invalid and username try again!")

    def sign():
        gui.destroy()
        signup()

    gui = Tk()
    gui.geometry("990x660+50+50")
    gui.resizable(0, 0)
    gui.title("INSTANT MESSAGING")
    gui.iconbitmap('favicon (1).ico')
    back = ImageTk.PhotoImage(file="loginback.jpg")
    backlablel = Label(gui, image=back)
    backlablel.place(x=0, y=0)
    head = Label(gui, text="USER LOGIN", fg="white")
    head.config(font=("Microsoft Yahei UI Light  that font", 23, "bold"), bg="#62ADF9")
    head.place(x=605, y=118)
    username_entery = Entry(gui, width=28, bg="#62ADF9", font=("Microsoft Yahei UI Light  that font", 11, "bold"),
                            fg="white", bd=0)
    username_entery.place(x=580, y=200)
    username_entery.insert(0, "Username")
    username_entery.bind('<FocusIn>', vider)
    frame1 = Frame(gui, width=250, height=2, bg="white")
    frame1.place(x=580, y=222)
    pass_enter = Entry(gui, width=28, bg="#62ADF9", font=("Microsoft Yahei UI Light  that font", 11, "bold"),
                       fg="white", bd=0)
    pass_enter.place(x=580, y=250)
    pass_enter.insert(0, "Password")
    pass_enter.bind("<FocusIn>", viderpass)
    frame1 = Frame(gui, width=250, height=2, bg="white")
    frame1.place(x=580, y=271)
    eyeop = ImageTk.PhotoImage(file="opeye.jpg")
    eyeclose = ImageTk.PhotoImage(file="closeeye.jpg")
    eyeopbutt = Button(gui, image=eyeop, bd=0, bg="#62ADF9", activebackground="#62ADF9", cursor="hand2", command=hide)
    eyeopbutt.place(x=800, y=245)
    #forget_butt = Button(gui, text="Forget Password?", bd=0, bg="#62ADF9", fg="white", activebackground="#62ADF9",
                        # cursor="hand2", font=("Microsoft Yahei UI Light  that font", 10, "bold"),
                        # activeforeground="white")
    #forget_butt.place(x=715, y=295)

    login_button = Button(gui, text="Login", cursor="hand2", font=("Open Sans", 16, "bold"), bg="white", fg="#62ADF9",
                          width=17, height=1, bd=0, activeforeground="#62ADF9", activebackground="white", command=login)
    login_button.place(x=591, y=340)
    or_use = Label(gui, text="------------- OR -------------", font=("Open Sans", 16, "bold"), fg="white", bg="#62ADF9")
    or_use.place(x=588, y=407)
    question = Label(gui, text="If you Don't have an account you can \n create yours from here!", fg="white",
                     bg="#62ADF9", font=("Microsoft Yahei UI Light  that font", 11, "bold"))
    question.place(x=575, y=445)
    create_butt = Button(gui, text="Create new account", cursor="hand2", fg="#001B79", bd=0, bg="#62ADF9",
                         activeforeground="white", activebackground="#62ADF9",
                         font=("Microsoft Yahei UI Light  that font", 11, "bold", "underline"), command=sign)
    create_butt.place(x=630, y=498)
    gui.bind('<Return>', lambda event=None: login())
    gui.mainloop()


def signup():
    def signfun():
        global name

        name = nameentry.get("1.0", "end")
        email = mailentry.get("1.0", "end")
        pasword = passentry.get("1.0", "end")
        name = name.strip()
        email = email.strip()
        pasword = pasword.strip()

        if name == '' or email == '' or pasword == '':
            messagebox.showerror("ERROR!", "enter all data")

        else:
            signup_data = [name, email, pasword]
            # Send the signup data to the server
            sock_client.send("seds".encode("utf-8"))
            time.sleep(0.1)
            json_str = json.dumps(signup_data)

            sock_client.send(json_str.encode("utf-8"))
            print("sdjk")

            rep = sock_client.recv(1024).decode("utf-8")
            rep = rep.strip()
            if rep == "er":
                messagebox.showerror("ERROR!", "username already exist")
            elif rep == "good":
                messagebox.showinfo("SUCCES", "account has been created")

            nameentry.delete("1.0", "end-1c")
            mailentry.delete("1.0", "end-1c")
            passentry.delete("1.0", "end-1c")

    def log():
        sighup.destroy()
        loginpage()

    sighup = Tk()

    sighup.resizable(0, 0)
    sighup.title("INSTANT MESSAGING")
    sighup.iconbitmap('favicon (1).ico')
    sighimage = ImageTk.PhotoImage(file="signnnnnnn.jpg")
    signlabel = Label(sighup, image=sighimage)
    sighup.geometry("990x660")
    signlabel.place(x=0, y=0)
    textlabel = Label(sighup, text="CREATE  ACCOUNT", font=("Californian FB", 18, "bold"), fg="#62ADF9", bg="white")
    textlabel.place(x=395, y=143)
    usernamelabel = Label(sighup, text="Username", font=("Californian FB", 13, "bold"), fg="#62ADF9", bg="white")
    usernamelabel.place(x=367, y=197)
    nameentry = Text(sighup, width=34, height=1.5, bg="#62ADF9", bd=0, fg="white")
    nameentry.place(x=367, y=230)
    emaillabel = Label(sighup, text="Email", font=("Californian FB", 13, "bold"), fg="#62ADF9", bg="white")
    emaillabel.place(x=365, y=270)
    mailentry = Text(sighup, width=34, height=1.5, bg="#62ADF9", bd=0, fg="white")
    mailentry.place(x=367, y=300)
    passwordlabel = Label(sighup, text="Password", font=("Californian FB", 13, "bold"), fg="#62ADF9", bg="white")
    passwordlabel.place(x=365, y=342)
    passentry = Text(sighup, width=34, height=1.5, bg="#62ADF9", bd=0, fg="white")
    passentry.place(x=367, y=370)
    sighbutt = Button(sighup, text="Sign Up", cursor="hand2", font=("Californian FB", 13, "bold"), fg="white",
                      bg="#62ADF9", activebackground="#62ADF9", bd=0, activeforeground="white", command=signfun)
    sighbutt.place(x=465, y=463)
    sighup.bind('<Return>', lambda event=None: signfun())
    qeustlabel = Label(sighup, text="I already have an account!", font=("Californian FB", 10, "bold"), fg="#62ADF9",
                       bg="white")
    qeustlabel.place(x=390, y=523)
    loginbutt = Button(sighup, text="Log in", font=("Microsoft Yahei UI Light  that font", 11, "bold", "underline"),
                       bd=0, bg="white", fg="#001B79", activeforeground="#001B79", activebackground="white",
                       cursor="hand2", command=log)
    loginbutt.place(x=539, y=520)
    sighup.mainloop()


gui_donne = False
control = True


def gui_loop():
    global gui_donne
    global sock_client
    global control
    global text_appear
    global textmess
    global chngename
    global create_room
    global public_butt
    global prive_butt
    global nom
    global scrollable_frame_crate
    global frame_salon
    root = tkinter.Tk()
    root.geometry("990x660+50+50")
    root.resizable(0, 0)
    root.title("INSTANT MESSAGING")
    root.iconbitmap('favicon (1).ico')
    back = ImageTk.PhotoImage(file="simple_chat.jpg")
    backlabel = Label(root, image=back)
    backlabel.place(x=0, y=0)

    text_appear = tkinter.scrolledtext.ScrolledText(root, height=32, width=64, bd=0)
    text_appear.place(x=444, y=55)
    text_appear.config(state="disabled")

    textmess = tkinter.Text(root, height=2.2, width=60, bd=0)
    textmess.place(x=432, y=602)

    def sending():
        global nom
        message = f"{nom}: {textmess.get('1.0', 'end')}"
        sock_client.send(message.encode("utf-8"))
        textmess.delete("1.0", "end")

    im = ImageTk.PhotoImage(file="Asset 1.png")
    sendbutt = tkinter.Button(root, image=im, command=sending, bg="#00ADEF", activebackground="#00ADEF", bd=0)
    sendbutt.config(font=("Arial", 12))
    sendbutt.place(x=925, y=588)


    gui_donne = True

    def stop():
        global control
        control = False
        root.destroy()
        sock_client.close()
        exit(0)

    root.protocol("WM_DELETE_WINDOW", stop)

    def menu():
        global mesgehistory
        global menufr
        global listconnect
        global mesgehistory
        global a
        global frame_salon
        global show_lista
        global chngename
        global create_room
        global public_butt
        global prive_butt
        global nom
        global disconnect
        global room_name
        global save_buttoon
        global scrollable_frame_crate
        global show_list_room
        global rooms
        global frame_salon
        global rom_name

        def hideframe():
            global show_lista
            menufr.destroy()
            menu_butt.config(text="\u0332\u0332\u0332")
            menu_butt.config(command=menu)
            show_lista.destroy()
            show_list_room.destroy()

        def disconnected():
            global control
            control = False
            root.destroy()
            sock_client.close()
            exit(0)


        menu_butt.config(text="x", command=hideframe)
        menufr = Frame(root, bg="white", height=585, width=201)
        menufr.place(x=0, y=76)
        listconnect = Button(menufr, text="CONNECTED USERS", font=("Arial", 12, "bold"), bd=0, fg="#00ADEF", bg="white",
                             activeforeground="#00ADEF",
                             activebackground="white", cursor="hand2", command=cheklist)
        listconnect.place(x=17, y=10)

        chngename = Button(menufr, text="NICKNAME CHANGE", cursor="hand2", font=("Arial", 12, "bold"), bd=0,
                           fg="#00ADEF",
                           bg="white", command=name_change)
        chngename.place(x=17, y=70)
        create_room = Button(menufr, text="CREATE ROOM", cursor="hand2", font=("Arial", 12, "bold"), bd=0, fg="#00ADEF",
                             bg="white", command=crete_roo)
        create_room.place(x=17, y=130)
        rooms = Button(menufr, text="ROOMS", cursor="hand2", font=("Arial", 12, "bold"), bd=0, fg="#00ADEF",
                       bg="white", command=hide_frmae_r)
        rooms.place(x=17, y=190)
        line = Frame(root, width=210, height=2, bg="#00ADEF")
        line.place(x=0, y=621)
        disconnect = Button(menufr, text="DISCONNECT", cursor="hand2", font=("Arial", 12, "bold"), bd=0, fg="#00ADEF",
                            bg="white", command=disconnected)
        disconnect.place(x=17, y=550)

        def on_enter(event):
            listconnect.config(bg="#00ADEF", fg="white", activebackground="#00ADEF", activeforeground="white")

        def on_leave(event):
            listconnect.config(fg="#00ADEF", bg="white")

        def on_enter3(event):
            chngename.config(bg="#00ADEF", fg="white", activebackground="#00ADEF", activeforeground="white")

        def on_leave3(event):
            chngename.config(fg="#00ADEF", bg="white")

        def on_enter4(event):
            create_room.config(bg="#00ADEF", fg="white", activebackground="#00ADEF", activeforeground="white")

        def on_leave4(event):
            create_room.config(fg="#00ADEF", bg="white")

        def on_enter5(event):
            disconnect.config(bg="#00ADEF", fg="white", activebackground="#00ADEF", activeforeground="white")

        def on_leave5(event):
            disconnect.config(fg="#00ADEF", bg="white")

        def on_enter6(event):
            rooms.config(bg="#00ADEF", fg="white", activebackground="#00ADEF", activeforeground="white")

        def on_leave6(event):
            rooms.config(fg="#00ADEF", bg="white")

        listconnect.bind("<Enter>", on_enter)
        listconnect.bind("<Leave>", on_leave)
        chngename.bind("<Enter>", on_enter3)
        chngename.bind("<Leave>", on_leave3)
        create_room.bind("<Enter>", on_enter4)
        create_room.bind("<Leave>", on_leave4)
        disconnect.bind("<Enter>", on_enter5)
        disconnect.bind("<Leave>", on_leave5)
        rooms.bind("<Enter>", on_enter6)
        rooms.bind("<Leave>", on_leave6)

    def crete_roo():
        global disconnect
        global room_name
        global save_buttoon
        global show_list_room
        global scrollable_frame_crate
        global rooms

        def hide_entry():
            rooms.place_forget()
            create_room.config(command=crete_roo)
            room_name.destroy()
            save_buttoon.destroy()
            rooms.place(x=17, y=190)
            show_list_room.destroy()

        rooms.place_forget()
        rooms.place(x=17, y=250)
        create_room.config(command=hide_entry)

        room_name = Entry(menufr, bg="white", bd=2, width=20)
        room_name.place(x=17, y=190)
        save_buttoon = Button(menufr, text="Save", bd=0, bg="#00ADEF", fg="white", font=("Arial", 10, "bold"),
                              activebackground="#00ADEF", activeforeground="white", command=room)
        save_buttoon.place(x=150, y=190)

    def room():
        global rom_name
        global show_list_room
        global rooms
        sock_client.send("r".encode("utf-8"))
        rom_name = room_name.get()
        sock_client.send(rom_name.encode("utf-8"))
        room_name.destroy()
        save_buttoon.destroy()
        rooms.place_forget()
        rooms.place(x=17, y=190)

    def frame_room(listu):
        global participant
        participant = [nom]

        def button_click_2(nnom):
            if nnom not in participant:
                participant.append(nnom)

        def create():
            print(participant)
            sock_client.send("--".encode("utf-8"))
            time.sleep(0.1)
            jsn_room = json.dumps(participant)
            sock_client.send(jsn_room.encode("utf-8"))
            show_list_room.destroy()

        def create_button_with_text_2(frame, text):

            button = Button(frame, text=text, bd=0, font=("Arial", 12, "bold"), bg="white", activebackground="white",
                            fg="#0073FC", activeforeground="#0073FC", command=lambda t=text: button_click_2(t))
            button.pack()

        show_list_room = Frame(root, bg="white", height=575, width=200)
        show_list_room.place(x=210, y=77)
        show_list_room.pack_propagate(False)
        canvas_creating_room = Canvas(show_list_room, bg="white", width=200, height=242)
        scrollbar = Scrollbar(show_list_room, orient="vertical", command=canvas_creating_room.yview)
        scrollable_frame_crate2 = Frame(canvas_creating_room, bg="white")
        scrollbar.pack(side="right", fill="y")
        canvas_creating_room.pack(side="left", fill="both", expand=True)
        canvas_creating_room.create_window((0, 0), window=scrollable_frame_crate2)
        scrollable_frame_crate2.bind("<Configure>",
                                     lambda e: canvas_creating_room.configure(
                                         scrollregion=canvas_creating_room.bbox("all")))

        for i in listu:
            if i != nom:
                create_button_with_text_2(scrollable_frame_crate2, i)

        save_butt = Button(scrollable_frame_crate2, text="CREATE", font=("Arial", 10, "bold"), width=10, bg="#00ADEF",
                           fg="white",
                           activeforeground="white", activebackground="#00ADEF", command=create)
        save_butt.pack(padx=70)

    def name_change():
        global new_names
        global save_button
        global rooms

        def hiding():
            create_room.place_forget()
            rooms.place_forget()
            new_names.destroy()
            save_button.destroy()
            create_room.place(x=17, y=130)
            rooms.place(x=17, y=190)

            chngename.config(command=name_change)

        chngename.config(command=hiding)
        create_room.place_forget()
        rooms.place_forget()
        create_room.place(x=17, y=190)
        rooms.place(x=17, y=250)
        new_names = Text(menufr, bd=2, bg="white", fg="black", height=1, width=20)
        new_names.place(x=17, y=120)
        save_button = Button(menufr, text="Save", bg="#00ADEF", bd=1, fg="white", font=("Arial", 10, "bold"),
                             activebackground="#00ADEF", activeforeground="white", command=changer)
        save_button.place(x=80, y=150)

    def changer():
        global new_names
        global nom
        nw = new_names.get('1.0', 'end')
        nw = nw.strip()
        if nw == '':
            messagebox.showerror("ERROR!", "ENTER NEW NAME!")
        else:
            new_names.destroy()
            save_button.destroy()
            create_room.place(x=17, y=130)
            rooms.place(x=17, y=190)
            chngename.config(command=name_change)
            sock_client.send("bdel".encode("utf-8"))
            time.sleep(0.1)

            print(nw)
            new_noms = [nom, nw]
            print(new_noms)
            jsn_nom = json.dumps(new_noms)
            sock_client.send(jsn_nom.encode("utf-8"))
            nom = nw.strip()

    def cheklist():
        sock_client.send("mconcti".encode("utf-8"))

    def mconecti(list_connected, all_client):
        global listconnect
        global show_lista
        global scrollable_frame_crate
        global i
        global j

        def hide_frame_mconcti():
            global show_lista
            show_lista.destroy()
            listconnect.configure(command=cheklist)

        def button_click(text):

            print(text)
            if text != "Pubic":
                sendbutt.config(command=lambda: sendprive(text))
                names = [nom, text]
                sock_client.send("hisprv".encode("utf-8"))
                time.sleep(0.1)
                jsn_n = json.dumps(names)
                sock_client.send(jsn_n.encode("utf-8"))

        def public():

            sendbutt.config(command=sending)
            sock_client.send("history".encode("utf-8"))

        def sendprive(text):
            global nom
            message = f"{nom}: {textmess.get('1.0', 'end')}#{text}"
            had = f"{nom}: {textmess.get('1.0', 'end')}"
            sock_client.send(message.encode("utf-8"))
            textmess.delete("1.0", "end")
            text_appear.config(state="normal")
            text_appear.insert("end", had)
            text_appear.yview("end")
            text_appear.config(state="disabled")

        def create_button_with_text(frame, text):
            if text == nom:
                button = Button(frame, text=f"     {text}", bd=1, width=19, font=("Arial", 12, "bold"), bg="white",
                                activebackground="white",
                                fg="#65B741", activeforeground="#65B741", command=lambda t=text: button_click(t))
                button.pack()
            else:
                button = Button(frame, text=f"     {text}", bd=1, width=19, font=("Arial", 12, "bold"), bg="white",
                                activebackground="white",
                                fg="#00ADEF", activeforeground="#00ADEF", command=lambda t=text: button_click(t))
                button.pack()

        def create_button_with_text_2(frame, text):

            button = Button(frame, text=f"     {text}", bd=1, width=19, font=("Arial", 12, "bold"), bg="white",
                            activebackground="white",
                            fg="#00ADEF", activeforeground="#00ADEF", state=DISABLED)
            button.pack()

        listconnect.config(command=hide_frame_mconcti)
        show_lista = Frame(root, bg="white", height=575, width=200)
        show_lista.place(x=210, y=77)
        show_lista.pack_propagate(False)
        canvas_creating = Canvas(show_lista, bg="white", width=200, height=242)
        scrollbar = Scrollbar(show_lista, orient="vertical", command=canvas_creating.yview)
        scrollable_frame_crate = Frame(canvas_creating, bg="white")
        scrollbar.pack(side="right", fill="y")
        canvas_creating.pack(side="left", fill="both", expand=True)
        canvas_creating.create_window((0, 0), window=scrollable_frame_crate)
        scrollable_frame_crate.bind("<Configure>",
                                    lambda e: canvas_creating.configure(scrollregion=canvas_creating.bbox("all")))
        button = Button(scrollable_frame_crate, text="       Broadcast", bd=1, width=19, font=("Arial", 12, "bold"),
                        bg="white",
                        activebackground="white",
                        fg="#00ADEF", activeforeground="#00ADEF", command=public)
        button.pack()

        for inner_list in all_client:
            for item in inner_list:
                if item in list_connected:
                    create_button_with_text(scrollable_frame_crate, item)
                else:
                    create_button_with_text_2(scrollable_frame_crate, item)

    menu_butt = Button(root, text="\u0332\u0332\u0332", font=("Arial", 30), bd=0, bg="#00ADEF", fg="white",
                       activebackground="#00ADEF", activeforeground="white", command=menu)
    menu_butt.place(x=11, y=5)

    def send_room(id_room):
        sendbutt.config(command=lambda id=id_room: sending_rooom(id))

    def sending_rooom(id_roomm):
        message = f"{nom}: {textmess.get('1.0', 'end')}@{id_roomm}"
        sock_client.send(message.encode("utf-8"))
        textmess.delete("1.0", "end")

    show_list_room_name = Frame(root, bg="white", height=575, width=200)
    show_list_room_name.place(x=210, y=77)
    show_list_room_name.pack_propagate(False)
    canvas_creating_room_name = Canvas(show_list_room_name, bg="white", width=200, height=242)
    scrollbar = Scrollbar(show_list_room_name, orient="vertical", command=canvas_creating_room_name.yview)
    scrollable_frame_crate3 = Frame(canvas_creating_room_name, bg="white")
    scrollbar.pack(side="right", fill="y")
    canvas_creating_room_name.pack(side="left", fill="both", expand=True)
    canvas_creating_room_name.create_window((0, 0), window=scrollable_frame_crate3)
    scrollable_frame_crate3.bind("<Configure>",
                                 lambda e: canvas_creating_room_name.configure(
                                     scrollregion=canvas_creating_room_name.bbox("all")))

    instat_room = Label(scrollable_frame_crate3, text="     INSTANT ROOMS", bd=2, width=19, font=("Arial", 12, "bold"),
                        bg="white",
                        activebackground="white",
                        fg="#00ADEF", activeforeground="#00ADEF", pady=6)
    instat_room.pack()
    show_list_room_name.place_forget()

    def crete(room_nameee):
        button_chat_room = Button(scrollable_frame_crate3, text=room_nameee, bd=1, width=19, font=("Arial", 12, "bold"),
                                  bg="white",
                                  activebackground="white",
                                  fg="#00ADEF", activeforeground="#00ADEF",
                                  command=lambda id=room_nameee: send_room(id))
        button_chat_room.pack()

    def hide_frmae_r():
        rooms.config(command=aff_frame_room)
        show_list_room_name.place(x=210, y=77)
       # rooms.config(command=aff_frame_room)
       # show_list_room_name.place_forget()

    def aff_frame_room():
        rooms.config(command=hide_frmae_r)
        show_list_room_name.place_forget()

        #rooms.config(command=hide_frmae_r)
        #show_list_room_name.place(x=210, y=77)

    def reci():
        global gui_donne
        global sock_client
        global control
        global text_appear
        global frame_salon
        global room_nameee
        while control:
            try:
                message = sock_client.recv(1024).decode("utf-8")
                print(message)

                if message == "zzzz":
                    json_eye = sock_client.recv(1024).decode("utf-8")
                    lista = json.loads(json_eye)

                    all_clien_jsn = sock_client.recv(1024).decode("utf-8")
                    all_client = json.loads(all_clien_jsn)
                    mconecti(lista, all_client)
                    print(lista)
                    print(all_client)

                if message == "historic":
                    print("trrrrrr")
                    jsn_historic = sock_client.recv(4096).decode("utf-8")
                    history_data = json.loads(jsn_historic)
                    print(history_data)
                    text_appear.config(state="normal")
                    text_appear.delete(1.0, "end")  # Use 1.0 instead of 0 for the ScrolledText widget
                    for item in history_data:
                        text_appear.insert("end", f"{item[0]}:{item[1].strip()}\n")  # Add newline after each entry
                    text_appear.yview("end")
                    text_appear.config(state="disabled")

                if message == "historicprv":

                    print("trrriiirrr")
                    jsn_historic_prv = sock_client.recv(4096).decode("utf-8")
                    history_data_prv = json.loads(jsn_historic_prv)
                    print(history_data_prv)
                    text_appear.config(state="normal")
                    text_appear.delete(1.0, "end")  # Use 1.0 instead of 0 for the ScrolledText widget
                    for item in history_data_prv:
                        text_appear.insert("end", f"{item[0]}:{item[1].strip()}\n")  # Add newline after each entry
                    text_appear.yview("end")
                    text_appear.config(state="disabled")

                if message == "nnnnn":
                    json_eyes = sock_client.recv(1024).decode("utf-8")
                    listi = json.loads(json_eyes)
                    print(listi)
                    frame_room(listi)

                if message == "butt":
                    room_nameee = sock_client.recv(1024).decode("utf-8")
                    print(room_nameee)
                    crete(room_nameee)
                # button_chat_room = Button(root, text=room_nameee, bd=0,
                #     font=("Arial", 12, "bold"), bg="white",
                #  activebackground="white", fg="#0073FC", activeforeground="#0073FC",
                # command=send_room)
                #   button_chat_room.pack()

                if message == "avec succes":
                    messagebox.showinfo("GOOD!", "YOUR NAME HAS BEEN CHANGED!")

                if gui_donne and message != "zzzz" and message != "historic" and message != "avec succes" and message != "historicprv" and message != "nnnnn" and message != "butt":
                    print("dkhelt")
                    text_appear.config(state="normal")
                    text_appear.insert("end", message)
                    text_appear.yview("end")
                    text_appear.config(state="disabled")
            except ConnectionAbortedError:
                break
            except Exception as e:
                print("error:", e)
                sock_client.close()
                break

    reci_thread = threading.Thread(target=reci)
    reci_thread.start()
    root.mainloop()


loginpage()
