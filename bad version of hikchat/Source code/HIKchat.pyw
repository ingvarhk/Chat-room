import mysql.connector
import tkinter as tk
from tkinter import messagebox
from functools import partial
from datetime import datetime
import threading
from time import sleep
import re
import requests
import json
#from PIL import Image, ImageTk
#from win10toast import ToastNotifier
import sys
import os
import urllib.request

currentVersion = "0.03"

print("Start")
loaded = False

#toaster = ToastNotifier()
def FileSetup():
#    Creating folders if they don't exists
    if not os.path.exists("data"):
        os.mkdir('data')
    if not os.path.exists("assets"):
        os.mkdir('assets')
    if not os.path.exists("extra"):
        os.mkdir('extra')
    if not os.path.exists("extra\\42"):
        os.mkdir('extra\\42')
    if not os.path.exists("extra\\test"):
        os.mkdir('extra\\test')
    if not os.path.exists("data\\friends"):
        os.mkdir('data\\friends')
        
#    If not user.data exists, then create it with standard values
    if not os.path.isfile("data\\user.data"):
        print("Missing file. user.data")
        userData = {}
        userData['user'] = []
        
        userData['user'].append({
            "loggedin": False,
            "username": "",
            "password": ""
        })
        userData['settings'] = []
        userData['settings'].append({
            "notifications": True,
            "runonstart": False
        })
        try:
            with open("data\\user.data", 'w+') as f:
                json.dump(userData, f)
                f.close()     
        except:
             print("Couldn't create user.data")
            
    
#    Downloading the HIKchat icon from ingvar.hahnkristensen.dk if not existing
    if not os.path.isfile("assets\\logo.ico"):
        try:
            urllib.request.urlretrieve("http://ingvar.hahnkristensen.dk/assets/logo.ico", "assets\\logo.ico")
        except Exception as e:
            print("Couldn't download logo.ico from ingvar.hahnkristensen.dk\n" + str(e))
    
#    Creting README
    try:
        readme = open("README", "w")
        readme.write("""Thanks for installing HIKchat!!
Version: """ + currentVersion + """
Copyright © 2019 Ingvar Hahn Kristensen. All rights reserved.

I hope you enjoy it and find find it useful.
..or.. you don't have to find it useful..
Anyway, may you have a good time with HIKchat!

________________**SPOILER ALERT**_________________
      There are a lot of bugs in HIKchat
________________**SPOILER ALERT**_________________


Check my website and other pages out:

https://github.com/hikbit
http://ingvar.hahnkristensen.dk
    """)
        readme.close()
    except:
        print("Couldn't create/update README")
        
    

def ServerConnection():
    url='http://ingvar.hahnkristensen.dk/'
    timeout=5
    try:
        requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        pass
    return False
 

def MysqlSetup():
    global mydb

    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="hikchat",
        buffered=False)
        print("Connected to the database")
    except:
        print("Failed connecting to database")
        print(" ")
        
def ReadJsonFile(path):
    try:
        with open(path, 'r') as f:
            LoadedData = json.load(f)
            f.close()
    except:
        LoadedData = "No data/coudn't load data"
        print("Coudn't load data from '" + path + "'")
    return LoadedData
    
def clear_entry(entry):
    entry.delete(0, tk.END)

def clear_entryPassword(entry):
    entry.delete(0, tk.END)
    entry.configure(show='•')


def SplashScreenSetup():
    global LoadingStuff
    global dots
    global loaded
    global serverProblem
    global splashRoot
    
    splashRoot = tk.Tk()
    dots = "◈"

    def LoadingDots():
        global LoadingStuff
        global dots
        global splashRoot
        global t
        
        if serverProblem == True:
            for widget in splashRoot.winfo_children():
                widget.destroy()
                
            print("splashRoot cleared")
            errorLoading = tk.Label(splashRoot, text="Couldn't connect\nto the server.", bg="#e59a3d", fg="black", font=("Arial", 15, "bold"), justify=tk.CENTER)
            errorLoading.place(x = 17, y = 20)
            errorLSymbol = tk.Label(splashRoot, text="⚠", bg="#e59a3d", fg="black", font=("Arial", 40, "bold"))
            errorLSymbol.place(x = 60, y = 80)
            
            TryAgain = tk.Button(splashRoot, relief=tk.FLAT, text ="Try again", font=("Arial", 13), bg="white", command = partial(tryAgainConnection, splashRoot))
            TryAgain.place(y=182, x=50, anchor=tk.CENTER, width=98, height=35)

            ExitButton = tk.Button(splashRoot, relief=tk.FLAT, text ="Exit", font=("Arial", 13), bg="white", command = partial(destroyWindow, splashRoot))
            ExitButton.place(y=182, x=150, anchor=tk.CENTER, width=100, height=35)            
            
        else:  
            if loaded:
                splashRoot.destroy()
                
                
            else:
            
                LoadingStuff['text'] = dots
                
                if len(dots) > 3:
                    dots = "◈"
                    splashRoot.after(500, LoadingDots)
                else:
                    dots = dots + "◈"
                    splashRoot.after(500, LoadingDots)
        
        
    
    splashRoot.overrideredirect(True)
    
    windowWidth = splashRoot.winfo_reqwidth()
    windowHeight = splashRoot.winfo_reqheight()
    positionRight = int(splashRoot.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(splashRoot.winfo_screenheight()/2.2 - windowHeight/2)
    splashRoot.geometry("+{}+{}".format(positionRight, positionDown))
    splashRoot.configure(background='#e59a3d')
    
    splashRoot.after(500, LoadingDots)
    
    headerLoading = tk.Label(splashRoot, text="Starting HIKchat", bg="#e59a3d", fg="black", font=("Arial", 15, "bold"), justify=tk.CENTER)
    headerLoading.place(x = 17, y = 20)
    
    LoadingStuff = tk.Label(splashRoot, text="", bg="#e59a3d", fg="black", font=("Arial", 50, "bold"), justify=tk.CENTER)
    LoadingStuff.place(x = 24, y = 85)

    splashRoot.mainloop()
      
def destroyWindow(window):
    window.destroy()

def tryAgainConnection(window):
    global serverProblem
    
    if ServerConnection():
        serverProblem = False
    else:
        serverProblem = True
    print(CurrentFile)
    os.startfile(CurrentFile)
    window.destroy()
    sys.exit()
    
    
     
class mainscreen:
    
    def __init__(self, master):
        
        global currentVersion
        global dataList
        
        self.dataList = ""
#        self.dataList = dataList
        
        self.loggetIn = False
        self.loggetInUserId = 0
        self.loggetInUsername = ""
        
        self.master = master
        
        self.master.protocol("WM_DELETE_WINDOW", self.onExit)
        
        self.master.geometry('300x400')
        self.master.resizable(0, 0)
        self.master.iconbitmap('assets\\logo.ico')
        self.master.title("HIKchat")
        
        self.loggingIn = False
        self.SigningIn = False
        self.TimesClickedEaster = 0
        
        UserData = ReadJsonFile("data\\user.data")
        
        

        
        if UserData['user'][0]['loggedin'] == True:
            self.loginScreenSetup()
            self.UserLogin(UserData['user'][0]['username'], UserData['user'][0]['password'])
            self.loggingIn = True
        else: 
            self.signupScreenSetup()
            self.SigningIn = True

    
    def loginScreenSetup(self):
        
        try:
            self.SignupCanvas.destroy()
        except:
            pass
        
        if self.TimesClickedEaster > 20:
            self.popupWindowTooManyTimesClicked()
            self.TimesClickedEaster = 0
        else:
            self.TimesClickedEaster += 1
        
        self.LoginCanvas = tk.Canvas(self.master, bg="#e59a3d", border=None, bd=0, highlightthickness=0, relief='ridge')
        self.LoginCanvas.pack(fill="both", expand=True)
    
#        usernameInputSignup = tk.Entry(LoginCanvas)
#        usernameInputSignup.place(x = 10, y = 10)
#        passwordInputSignup = tk.Entry(LoginCanvas)
#        passwordInputSignup.place(x = 10, y = 40)
#        ClickMeSignup = tk.Button(LoginCanvas, text ="Sign Up", command = partial(SignupButton, usernameInputSignup, passwordInputSignup))
#        ClickMeSignup.place(x = 10, y = 65)
#    
#        SignUpErrorText = tk.Label(LoginCanvas, text="", fg="red", bg="#e59a3d", font=("Helvetica", 10), justify=tk.LEFT)
#        SignUpErrorText.place(x = 10, y = 100)
    
        self.header1 = tk.Label(self.LoginCanvas, text="Login", bg="#e59a3d", fg="black", font=("Arial", 20, "bold"), justify=tk.LEFT)
        self.header1.place(y=100, relx=0.5, anchor=tk.CENTER)
    
        self.usernameInputLogin = tk.Entry(self.LoginCanvas, font=("Arial", 13), relief=tk.FLAT, bd=1)
        self.usernameInputLogin.place(y=150, relx=0.5, anchor=tk.CENTER, width=200, height=35)
    
        self.usernameInputLogin.insert(0, " Username")
        self.usernameInputLogin.bind("<Button-1>", lambda event: clear_entry(self.usernameInputLogin))
        self.usernameInputLogin.bind("<Tab>", lambda event: clear_entryPassword(self.passwordInputLogin))
    
    
        self.passwordInputLogin = tk.Entry(self.LoginCanvas, font=("Arial", 13), relief=tk.FLAT)
        self.passwordInputLogin.place(y=200, relx=0.5, anchor=tk.CENTER, width=200, height=35)
    
        self.passwordInputLogin.insert(0, " Password")
        self.passwordInputLogin.bind("<Button-1>", lambda event: clear_entryPassword(self.passwordInputLogin))
    
    
        self.ClickMeLogin = tk.Button(self.LoginCanvas, relief=tk.FLAT, text ="OK", font=("Arial", 13), bg="white", command = partial(self.LoginButton, self.usernameInputLogin, self.passwordInputLogin))
        self.ClickMeLogin.place(y=250, relx=0.5, anchor=tk.CENTER, width=200, height=35)
        
#        self.text1 = tk.Label(self.LoginCanvas, text="Version " + currentVersion + "\nCopyright © 2019 Ingvar Hahn Kristensen.\nAll rights reserved.", bg="#e59a3d", fg="black", font=("Arial", 9), justify=tk.LEFT)
#        self.text1.place(y=348, x = 5)
#        
        self.SignUpInstead = tk.Button(self.LoginCanvas, borderwidth=0, relief="solid", text ="Sign Up", bg="white", font=("Arial", 10), command = partial(self.signupScreenSetup))
        self.SignUpInstead.place(y=365, x=0, width=300, height=35)
        
        self.LogInErrorText = tk.Label(self.LoginCanvas, text="", fg="red", bg="#e59a3d", font=("Helvetica", 11), justify=tk.LEFT)
        self.LogInErrorText.place(x = 30, y = 280)
    
    def signupScreenSetup(self):
        
        try:
            self.LoginCanvas.destroy()
        except:
            pass
        
        if self.TimesClickedEaster > 20:
            self.popupWindowTooManyTimesClicked()
            self.TimesClickedEaster = 0
        else:
            self.TimesClickedEaster += 1
        
        self.SignupCanvas = tk.Canvas(self.master, bg="#e59a3d", border=None, bd=0, highlightthickness=0, relief='ridge')
        self.SignupCanvas.pack(fill="both", expand=True)
    
#        usernameInputSignup = tk.Entry(LoginCanvas)
#        usernameInputSignup.place(x = 10, y = 10)
#        passwordInputSignup = tk.Entry(LoginCanvas)
#        passwordInputSignup.place(x = 10, y = 40)
#        ClickMeSignup = tk.Button(LoginCanvas, text ="Sign Up", command = partial(SignupButton, usernameInputSignup, passwordInputSignup))
#        ClickMeSignup.place(x = 10, y = 65)
#    
#        SignUpErrorText = tk.Label(LoginCanvas, text="", fg="red", bg="#e59a3d", font=("Helvetica", 10), justify=tk.LEFT)
#        SignUpErrorText.place(x = 10, y = 100)
    
        self.header2 = tk.Label(self.SignupCanvas, text="Sign Up", bg="#e59a3d", fg="black", font=("Arial", 20, "bold"), justify=tk.LEFT)
        self.header2.place(y=100, relx=0.5, anchor=tk.CENTER)
    
#       #########
        
        self.NewUsernameInputLogin = tk.Entry(self.SignupCanvas, font=("Arial", 13), relief=tk.FLAT, bd=1)
        self.NewUsernameInputLogin.place(y=150, relx=0.5, anchor=tk.CENTER, width=200, height=35)
    
        self.NewUsernameInputLogin.insert(0, " New Username")
        self.NewUsernameInputLogin.bind("<Button-1>", lambda event: clear_entry(self.NewUsernameInputLogin))
        self.NewUsernameInputLogin.bind("<FocusIn>", lambda event: clear_entry(self.NewUsernameInputLogin))
        
#       #########    
        
        self.NewPasswordInputLogin = tk.Entry(self.SignupCanvas, font=("Arial", 13), relief=tk.FLAT)
        self.NewPasswordInputLogin.place(y=200, relx=0.5, anchor=tk.CENTER, width=200, height=35)
    
        self.NewPasswordInputLogin.insert(0, " New Password")
        self.NewPasswordInputLogin.bind("<Button-1>", lambda event: clear_entryPassword(self.NewPasswordInputLogin))
        self.NewPasswordInputLogin.bind("<FocusIn>", lambda event: clear_entryPassword(self.NewPasswordInputLogin))
#       #########
        
        self.NewPasswordInputLoginRepeat = tk.Entry(self.SignupCanvas, font=("Arial", 13), relief=tk.FLAT)
        self.NewPasswordInputLoginRepeat.place(y=250, relx=0.5, anchor=tk.CENTER, width=200, height=35)
    
        self.NewPasswordInputLoginRepeat.insert(0, " Repeat..")
        self.NewPasswordInputLoginRepeat.bind("<Button-1>", lambda event: clear_entryPassword(self.NewPasswordInputLoginRepeat))
        self.NewPasswordInputLoginRepeat.bind("<FocusIn>", lambda event: clear_entryPassword(self.NewPasswordInputLoginRepeat))
#       #########
    
    
        self.ClickMeSignup = tk.Button(self.SignupCanvas, relief=tk.FLAT, text ="OK", font=("Arial", 13), bg="white", command = partial(self.SignupButton, self.NewUsernameInputLogin, self.NewPasswordInputLogin, self.NewPasswordInputLoginRepeat))
        self.ClickMeSignup.place(y=300, relx=0.5, anchor=tk.CENTER, width=200, height=35)
        
        self.SignUpErrorText = tk.Label(self.SignupCanvas, text="", fg="red", bg="#e59a3d", font=("Helvetica", 11), justify=tk.LEFT)
        self.SignUpErrorText.place(x = 30, y = 330)
        
        self.SignUpInstead = tk.Button(self.SignupCanvas, borderwidth=0, relief="solid", text ="Log in", bg="white", font=("Arial", 10), command = partial(self.loginScreenSetup))
        self.SignUpInstead.place(y=365, x=0, width=300, height=35)
        
    def popupWindowTooManyTimesClicked(self):
        messagebox.showinfo("Stoooooop!!", "That's way too much for my brain.\nIf you click one more time...", parent = self.master)
        
    def rootHomeScreenSetup(self):
        if self.loggingIn:
            self.LoginCanvas.destroy()
        elif self.SigningIn:
            self.SignupCanvas.destroy()
    
        self.WelcomeScreen = tk.Canvas(self.master, bg="#e59a3d", border=None, bd=0, highlightthickness=0)
        self.WelcomeScreen.pack(fill="both", expand=True)
    
    
        menubar = tk.Menu(self.WelcomeScreen)
    
        usermenu = tk.Menu(menubar, tearoff=0)
        usermenu.add_command(label="Help")
        usermenu.add_command(label="Settings")
        usermenu.add_separator()
        usermenu.add_command(label="Log off", command = partial(self.CompleteUserLogoff))
        menubar.add_cascade(label="User", menu=usermenu)
    
        contactsmenu = tk.Menu(menubar, tearoff=0)
        contactsmenu.add_command(label="Recent")
        contactsmenu.add_command(label="All friends")
        contactsmenu.add_separator()
        contactsmenu.add_command(label="Add friend")
        menubar.add_cascade(label="Friends", menu=contactsmenu)
    
        messagemenu = tk.Menu(menubar, tearoff=0)
        messagemenu.add_command(label="New chat", command = partial(self.SendMesseage, 2, self.loggetInUserId, "testMessage"))
        messagemenu.add_command(label="All sent")
        menubar.add_cascade(label="Chat", menu=messagemenu)
    
        self.master.config(menu=menubar)
    
        header1 = tk.Label(self.WelcomeScreen, text="Welcome " + self.loggetInUsername + "!", bg="#e59a3d", fg="black", font=("Arial", 20, "bold"), justify=tk.LEFT)
        header1.place(x = 13, y = 10)
        
        recentText = tk.Label(self.WelcomeScreen, text="Recent chats:", bg="#e59a3d", fg="black", font=("Arial", 14, "bold"), justify=tk.LEFT)
        recentText.place(x = 20, y = 57)
#        UpdateButton = tk.Button(self.WelcomeScreen, relief=tk.FLAT, text ="Update", font=("Arial", 13), bg="white", command = partial(self.ShowRecentChats))
#        UpdateButton.place(y=60, x=40, width=200, height=35)
        
        textAtBottom = tk.Label(self.WelcomeScreen, text="To update you will have to quit and run HIKchat again.\nThis will be fixed very soon.", bg="#e59a3d", fg="white", font=("Arial", 8, "bold"))
        textAtBottom.place(x = 3, y = 347)
        

        
#        self.scrollbar = tk.Scrollbar(self.RecentChats)
#        self.RecentChats.configure(yscrollcommand=self.scrollbar)
#        
#   
#        self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
#        self.scrollbar.config(command=self.RecentChats.yview)
#        
#        self.RecentChats.configure(scrollregion=self.RecentChats.bbox("all"))
        self.ShowRecentChats()
        
                                            
#        w = Text ( master, option, ... )
    def ShowRecentChats(self):
        
        if self.loggetIn:
            
            self.RecentChats = tk.Canvas(self.master, width=256, height=251, bg="#acacac", relief=tk.FLAT, highlightthickness=1, borderwidth=1, highlightbackground="black", highlightcolor="black")
            self.RecentChats.place(x=20, y=90)
            print("New Canvas created")
            
            self.RecentChats.after(10000, self.ShowRecentChats)
    

            
            listOfRecentChatsUserName = []
            chatFromUsername = ""
            
            sql = "SELECT * FROM messages WHERE touserid = '" + str(self.loggetInUserId) + "' ORDER BY time DESC"
            userCursor = mydb.cursor(buffered=False)
            userCursor.execute(sql)
            allRows = userCursor.fetchall()
            
            
            listOfRecentChatsUserName = []
            yPosistionRectangels = 0
            
            for row in allRows:
    #            print(row)
                if not len(listOfRecentChatsUserName) > 4:
                    
                    sql = "SELECT * FROM users WHERE id = '" + row[3] + "'"
                    userCursor = mydb.cursor(buffered=False)
                    userCursor.execute(sql)
                    selectedUserResult = userCursor.fetchall()
                    
                    
                    for row in selectedUserResult:
                        
                        chatFromUsername = row[1]
                        
                        if not chatFromUsername in listOfRecentChatsUserName:
                            listOfRecentChatsUserName.append(chatFromUsername)
                            chatButton = tk.Button(self.RecentChats, relief=tk.FLAT, text = str(chatFromUsername) + " ", font=("Arial", 10), bg="white")
                            chatButton.place(height = 45, width = 250, x=5, y=5 + yPosistionRectangels)
                            yPosistionRectangels += 50
                            print(listOfRecentChatsUserName)
                else:
                    print("Recent chats loaded/updated")
                    return
            else:
                self.RecentChats.destroy()
        
    
    def UserLogin(self, username, password):

        userCursor = mydb.cursor(buffered=True)
        sql = "SELECT * FROM users WHERE username ='%s' AND password ='%s'" % (username, password)
        userCursor.execute(sql)
    
        usersOutput = userCursor.fetchall()
    
        if userCursor.rowcount > 0:
            for row in usersOutput:
    
                self.loggetInUserId = row[0]
                self.loggetInUsername = row[1]
    
                OnlineCursor = mydb.cursor()
                OnlineSql = "UPDATE users SET status = 1 WHERE id = '" + str(self.loggetInUserId) + "'"
                OnlineCursor.execute(OnlineSql)
    
                mydb.commit()
                
                userData = {}
                userData['user'] = []
                
                userData['user'].append({
                    "loggedin": True,
                    "username": username,
                    "password": password
                })
                try:
                    with open("data\\user.data", 'w+') as f:
                        json.dump(userData, f)
                        f.close()     
                except:
                    print("Couldn't update user.data with username and password.")
    
    
                print("Id: " + str(row[0]))
                print("Username: " + row[1])
                print("Password: " + row[2])
                self.loggetIn = True
                print("Log on")
                self.LoginCanvas.destroy()
                self.rootHomeScreenSetup()
                
                
        else:
            print("Username or password was incorrect")
            self.LogInErrorText['text'] = 'Username or password was incorrect'
            
            
    
    def LoginButton(self, usernameInputLogin, passwordInputLogin):
    
        username = usernameInputLogin.get()
        password = passwordInputLogin.get()
    
        self.UserLogin(username, password)
    
    
    
    def UserSignUp(self, NewUsername, NewPassword):
    
        if re.match("^[A-Za-z0-9_-]*$", NewUsername):
    
            IfExistUserCursor = mydb.cursor(buffered=True)
            sql = "SELECT * FROM users WHERE username = '" + NewUsername + "'"
            IfExistUserCursor.execute(sql)
    
            if IfExistUserCursor.rowcount == 0:
                NewUserCursor = mydb.cursor()
                sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                val = (NewUsername, NewPassword)
                NewUserCursor.execute(sql, val)
                mydb.commit()
    
                print("User was created")
                self.UserLogin(NewUsername, NewPassword)
            else:
                print("The username is already taken")
                self.SignUpErrorText['text'] = 'The username, "' + NewUsername + '" , is already taken'
        else:
            print("The username is not valid")
            self.SignUpErrorText['text'] = 'The username is not valid. Do only use\nletters (a-z), numbers(0-9),\nunderscores and dashes'
    
    def SignupButton(self, usernameInputSignup, passwordInputSignup, passwordInputSignupRepeat):
    
        newUsername = usernameInputSignup.get()
        newPassword = passwordInputSignup.get()
        newPasswordRepeat = passwordInputSignupRepeat.get()
        
        if newPassword == newPasswordRepeat:
            self.UserSignUp(newUsername, newPassword)
            pass
        else:
            self.SignUpErrorText['text'] = "The passwords aren't matching :("
            print("The passwords aren't matching :(")
        
        
    def UserLogoff(self):
        
        if self.loggetIn:
            self.loggetIn = False
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            OffLineCursor = mydb.cursor()
            OfflineSql = "UPDATE users SET status = 0 WHERE id = '" + str(self.loggetInUserId) + "'"
            OffLineCursor.execute(OfflineSql)
            
            OfflineSql2 = "UPDATE users SET lastonline = '" + timestamp + "' WHERE id = '" + str(self.loggetInUserId) + "'"
            OffLineCursor.execute(OfflineSql2)
            mydb.commit()
            
            print("Log off")
            
            self.WelcomeScreen.destroy()
            self.RecentChats.destroy()
            self.loginScreenSetup()
            
    def CompleteUserLogoff(self):
        
        if self.loggetIn:
            self.loggetIn = False
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            OffLineCursor = mydb.cursor()
            OfflineSql = "UPDATE users SET status = 0 WHERE id = '" + str(self.loggetInUserId) + "'"
            OffLineCursor.execute(OfflineSql)
            
            OfflineSql2 = "UPDATE users SET lastonline = '" + timestamp + "' WHERE id = '" + str(self.loggetInUserId) + "'"
            OffLineCursor.execute(OfflineSql2)
            mydb.commit()
    
            
            
            userData = {}
            userData['user'] = []
            
            userData['user'].append({
                "loggedin": False,
                "username": "",
                "password": ""
            })
            try:
                with open("data\\user.data", 'w+') as f:
                    json.dump(userData, f)
                    f.close()     
            except:
                print("Couldn't update user.data with username and password.")
            
            print("Complete log off completed")
            
            self.WelcomeScreen.destroy()
            self.loginScreenSetup()
            
    def SendMesseage(self, toUserId, fromUserId, content):
        print("Starting message sending..")
        messageCursor = mydb.cursor(buffered=False)
        sql = "INSERT INTO messages (fromuserid, touserid, content) VALUES (%s, %s, %s)"
        val = (fromUserId, toUserId, content)
        messageCursor.execute(sql, val)
        mydb.commit()
        print("Message sent :)")
          
    def onExit(self):
        self.UserLogoff()
        self.master.destroy()
 
def main():
    global loaded
    global serverProblem
    
    t = threading.Thread(target=SplashScreenSetup)
    t.start()
    
    FileSetup()
    
    if ServerConnection() == True:  
        MysqlSetup()
        
        serverProblem = False
        print("Connected to the server. Internet is on")
        
        sleep(3)
    
        print("Loading finished")
        
        loaded = True
#        t.join()
        
        root = tk.Tk()
        mainscreen(root)
        root.mainloop()
        
    else:
        serverProblem = True
        print("Couldn't connect to the server. Please check your internet connction")
        
if __name__ == '__main__':
    print("HIKchat " + currentVersion)
    CurrentFile = __file__
    main()
