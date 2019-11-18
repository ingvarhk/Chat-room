import socket
import threading
from functools import partial
import tkinter as tk
from tkinter import messagebox
import random
import sys
import os
import webbrowser
    
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
                chat.insert(tk.END, recived + "\n", 'server')
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
    webbrowser.open('http://ingvar.xyz/hikchat/server')
    
def sendChat():
    global inputUser
    global chat
    inputFromUser = inputUser.get()
    if inputFromUser.isspace() or inputFromUser == "":
        print("space!!")
        return
        
    inputUser.delete(0, 'end')
    try:
        inputFromUser = username + " >> " + inputFromUser 
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
        messagebox.showwarning("Not a valid username", "Please type a valid username.")
        return
    
    print("Connecting..")
    print(ip + port + "\nUsername: " + username)
    
    try:
        s.connect((ip, int(port)))
        print("\nSuccesfully connected!")

    except Exception:
        print("Could'nt connect. Please check the ip and the port.\n")
        messagebox.showwarning("Could not connect", "Please check if the ip and the port is correct")
        InputIp.delete(0, 'end')
        InputPort.delete(0, 'end')
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
    
    main.iconbitmap('assets/logo.ico')
    
    main.protocol("WM_DELETE_WINDOW", onExit)
    
    header1 = tk.Label(main, text="Server info", justify=tk.LEFT, font="Arial 12 bold")
    header1.place(y=10, x=3)
    info1 = tk.Label(main, text="Server name: " + title + "\nDescription: " + des + "\nIp: " + ip + "\nPort: " + port, justify=tk.LEFT, font=("Arial", 10))
    info1.place(y=30, x=7)
    
    header2 = tk.Label(main, text="User info", justify=tk.LEFT, font="Arial 12 bold")
    header2.place(y=120, x=3)
    info2 = tk.Label(main, text="Username: " + username + "\nOwn ip: " + IPAddr, justify=tk.LEFT, font=("Arial", 10))
    info2.place(y=140, x=7)
    
    header3 = tk.Label(main, text="Help", justify=tk.LEFT, font="Arial 12 bold")
    header3.place(y=200, x=3)
    info3 = tk.Label(main, text="Read the most frequently\nasked questions at\nhttp://ingvar.xyz/hikchat.\n\n", justify=tk.LEFT, font=("Arial", 10))
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
    
    
    chat.insert(tk.END, "Server >> Welcome to " + title + "!\n", 'server')
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
    creditsTk.iconbitmap('assets/logo.ico')
    
    
    
    header = tk.Label(creditsTk, text="Credits", justify=tk.LEFT, font="Arial 20 bold")
    header.place(y=5, x=145)
    
    information = tk.Label(creditsTk, text="Made by Ingvar Hahn Kristensen 2019\nYou are allowed to copy this as much as you want :)\n", font=("Arial", 10))
    information.place(y=50, x=45)
    
    link = tk.Label(creditsTk, text="http://ingvar.xyz/hikchat", font=("Arial", 10), fg="blue", cursor="hand2")
    link.place(y=100, x=120)
    link.bind("<Button-1>", lambda event: webbrowser.open_new("http://ingvar.xyz/hikchat"))
    
    
    
    creditsTk.mainloop()
    
def joinGUI():
    global join
    
    join = tk.Tk()
    join.title("Connect to server - HIKchat")
    join.resizable(height=False, width=False)
    join.geometry("400x190")
    join.iconbitmap('assets/logo.ico')

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
    ipInput.insert(tk.END, "")
    
    portInput = tk.Entry(join, font=("Arial", 9))
    portInput.place(y=30, x=150, width=60, height=30)
    
    names = ["Trump123", "PeterIsAwesome", "John_love_cake", "Santa_Claus", "Daddy134", "Dr. Bombay", "i_have_no_name"]
    name = random.choice(names)
    
    usernameInput = tk.Entry(join, font=("Arial", 9))
    usernameInput.place(y=100, x=10, width=200, height=30)
    usernameInput.insert(tk.END, name)
    
    connectButton = tk.Button(join, text="Connect", command = partial(Connect, ipInput, portInput, usernameInput))
    connectButton.place(y=143, x=10, width=200, height=30)
    
    join.mainloop()


if not os.path.exists('assets'):
    os.mkdir('assets')
    print("Missing file..")

title = "hejsa"
    
s = socket.socket()
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)
joinGUI()

