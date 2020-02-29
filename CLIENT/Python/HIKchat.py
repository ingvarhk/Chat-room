print("GO!")

import socket
import threading
from functools import partial
import tkinter as tk
from tkinter import messagebox
import sys
import os
import webbrowser

home_dir = os.path.dirname(sys.argv[0])

def newChats():
    global chat
    global userList
    global exitApp
    global title
    global des
    
    exitApp = False
    
    while True:
        if exitApp == True:
            break
        try:
            recived = s.recv(1024).decode("utf-8")
            
            if recived.startswith("servernameanddescription/") and "¤" in recived:
                print("title and description recived")
                titleAndDes = recived.replace("servernameanddescription/", "")
                title, des, trash = titleAndDes.split("¤")
                print("\n\n" + title + "\n" + des + "\n\n")
                
            elif recived.startswith("newjoined/"):
                print(recived)
                msgJoin = recived.replace("newjoined/", "")
                chat.config(state=tk.NORMAL)
                chat.insert(tk.END, msgJoin, 'newjoined')
                chat.config(state=tk.DISABLED)
                chat.see(tk.END)
                        
                
            elif recived.startswith("Server >>"):
                print(recived)
                chat.config(state=tk.NORMAL)
                chat.insert(tk.END, recived.replace(">", "", 1) + "\n", 'server')
                chat.config(state=tk.DISABLED)
                chat.see(tk.END)
                        
            else:
                print(recived)
                chat.config(state=tk.NORMAL)
                chat.insert(tk.END, recived + "\n")
                chat.config(state=tk.DISABLED)
                chat.see(tk.END)
        except:
            continue
        
def hostServerButton():
    webbrowser.open('https://github.com/ingvarhk/Chatroom/tree/master/SERVER')
    
def sendChat():
    global inputUser
    global chat
    inputFromUser = inputUser.get()
    if inputFromUser.isspace() or inputFromUser == "":
        print("space!!")
        return
        
    inputUser.delete(0, 'end')
    try:
        inputFromUser = username + " > " + inputFromUser 
        s.sendall(inputFromUser.encode())
    except:
        print("Couldnt send message")
        chat.config(state=tk.NORMAL)
        chat.insert(tk.END, "Couldn't send message. Try reconnecting to the server.\n", 'server')
        chat.config(state=tk.DISABLED)
        chat.see(tk.END)
        

def Connect(InputIp, InputPort, InputUsername):
    global username
    global ip
    global port
    

    
    global newChatsThread
    ip = InputIp.get()
    port = InputPort.get()
    username = InputUsername.get()
    
    if username.isspace() or username == "":
        print("space!!")
        messagebox.showwarning("Not a valid username", "Please enter a valid username.")
        return
    
    print("Connecting..")
    print(ip + port + "\nUsername: " + username)
    
    try:
        s.connect((ip, int(port)))
        print("\nSuccesfully connected!")

    except Exception:
        print("Couldn't connect. Please check the ip and the port.\n")
        messagebox.showwarning("Couldn't connect", "The server may be down. Check your internet connection.")
        return
        
    try:
        sendUsername = "username/" + username
        s.sendall(sendUsername.encode())
        print("username sent")
    except:
        print("Username could not be sent")

    join.destroy()
    
    newChatsThread = threading.Thread(target=newChats)
    newChatsThread.start()
    mainGUI()
        
        
def onExit():
    global exitApp
    exitApp = True

    print("Exiting..")
    try:
        sendExit = "exit/" + username
        s.sendall(sendExit.encode())
        print("exit sent")
#        s.close()
    except:
        print("Username could not be sent")
    
    main.destroy()
    sys.exit()
    
def mainGUI():
    global chat
    global inputUser
    global main
    global ip
    global port
    global des
    global title
    global IPAddr
    global username
    global inputUser
    
    if title == "":
        title = "The Server"
    
    main = tk.Tk()
    main.title(title + " - HIKchat")
    main.resizable(height=False, width=False)
    main.geometry("800x500")
    
    try:
        main.iconbitmap(home_dir + '/logo.ico')
    except Exception as e:
        print(e)
    
    main.protocol("WM_DELETE_WINDOW", onExit)
    
    header1 = tk.Label(main, text="Server info", justify=tk.LEFT, font="Arial 12 bold")
    header1.place(y=10, x=5)
    info1 = tk.Label(main, text="Server name: " + title + "\nDescription: " + des + "\nIp: " + ip + "\nPort: " + port, justify=tk.LEFT, font=("Arial", 10))
    info1.place(y=30, x=7)
    
    header2 = tk.Label(main, text="User info", justify=tk.LEFT, font="Arial 12 bold")
    header2.place(y=120, x=5)
    info2 = tk.Label(main, text="Username: " + username + "\nOwn ip: " + IPAddr, justify=tk.LEFT, font=("Arial", 10))
    info2.place(y=140, x=7)
    
    header3 = tk.Label(main, text="Help", justify=tk.LEFT, font="Arial 12 bold")
    header3.place(y=200, x=5)
    info3 = tk.Label(main, text="Unfortunately there is no\nhelp avaiable.. But you don't\nneed it. Do you? \n\n", justify=tk.LEFT, font=("Arial", 10))
    info3.place(y=220, x=7)
    
    creditsButton = tk.Button(main, text="Credits", command=creditsWindow)
    creditsButton.place(y=440, x=0, width=100, height=30)
    
    creditsButton = tk.Button(main, text="Host server", command=hostServerButton)
    creditsButton.place(y=440, x=100, width=100, height=30)
    
    disconnect = tk.Button(main, text="Disconnect", command=onExit)
    disconnect.place(y=470, x=0, width=200, height=30)
    
    chat = tk.Text(main, font=("Arial", 10))
    chat.place(height=470, width=600, x=200)
    
    chat.tag_config('newjoined', foreground="blue")
    chat.tag_config('server', foreground="red")
    
    
    chat.insert(tk.END, "Server > Welcome to " + title + "!\n", 'server')
    chat.config(state=tk.DISABLED)
    
    inputUser = tk.Entry(main, font=("Arial", 10))
    inputUser.place(y=470, x=200, width=500, height=30)
    inputUser.bind("<Return>", lambda event: sendChat())
    
    send = tk.Button(main, text="Send", command=sendChat)
    send.place(y=470, x=700, width=100, height=30)
    main.mainloop()

def hyperLink():
    webbrowser("http://ingvar.xyz/hikchat")
    
def creditsWindow():
    global creditsTk
    creditsTk = tk.Tk()
    creditsTk.title("Credits - HIKchat")
    creditsTk.resizable(height=False, width=False)
    creditsTk.geometry("400x190")
    
    try:
        creditsTk.iconbitmap(home_dir + '/logo.ico')
    except Exception as e:
        print(e)
    
    
    
    header = tk.Label(creditsTk, text="Credits", justify=tk.LEFT, font="Arial 20 bold")
    header.place(y=13, x=145)
    
    information = tk.Label(creditsTk, text="Made by Ingvar Hahn Kristensen 2019\nThanks for using HIKchat!\nVisit my website for more stuff like this.", font=("Arial", 10))
    information.place(y=80, relx=0.5, anchor=tk.CENTER)
    
    link = tk.Label(creditsTk, text="https://ingvar.xyz", font=("Arial", 10), fg="blue", cursor="hand2")
    link.place(y=130, relx=0.5, anchor=tk.CENTER)
    link.bind("<Button-1>", lambda event: webbrowser.open_new("http://ingvar.xyz"))
    
    
    
    creditsTk.mainloop()
    
def joinGUI():
    global join
    
    join = tk.Tk()
    join.title("Connect to server - HIKchat")
    join.resizable(height=False, width=False)
    join.geometry("400x190")
    
    try:
        join.iconbitmap(home_dir + '/logo.ico')
    except Exception as e:
        print(e)

    labelStuff = tk.Label(join, text="IP-adress", justify=tk.LEFT, font=("Arial", 10))
    labelStuff.place(y=10, x=8)
    
    labelStuff2 = tk.Label(join, text="Port", justify=tk.LEFT, font=("Arial", 10))
    labelStuff2.place(y=10, x=147)
    
    labelStuff3 = tk.Label(join, text="Username", justify=tk.LEFT, font=("Arial", 10))
    labelStuff3.place(y=80, x=8)
    
    informationHeader = tk.Label(join, text="Connect a server", justify=tk.LEFT, font="Arial 10 bold")
    informationHeader.place(y=10, x=220)
    
    information = tk.Label(join, text="To connect to a server you\nwill need the server's ip\nand the port. The username\nwill be displayed in the\nserver you join.\n\nRead more at\nhttp://ingvar.xyz/hikchat", justify=tk.LEFT, font=("Arial", 10))
    information.place(y=30, x=220)
    
    ipInput = tk.Entry(join, font=("Arial", 9))
    ipInput.place(y=30, x=10, width=130, height=30)
    ipInput.insert(tk.END, "chat.ingvar.xyz")
    
    portInput = tk.Entry(join, font=("Arial", 9))
    portInput.place(y=30, x=150, width=60, height=30)
    portInput.insert(tk.END, "56000")
    
    usernameInput = tk.Entry(join, font=("Arial", 9))
    usernameInput.place(y=100, x=10, width=200, height=30)
    usernameInput.focus()
    
    connectButton = tk.Button(join, text="Connect", command = partial(Connect, ipInput, portInput, usernameInput))
    connectButton.place(y=143, x=10, width=200, height=30)
    
    join.mainloop()

title = "Title not recived"
    
s = socket.socket()
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)
joinGUI()

