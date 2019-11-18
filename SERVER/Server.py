print("importing libraries..")
import socket
import threading
import os
import sys
  
#import datetime
def fileStuff():
    global settings
    settings = []
    while True:
        if os.path.exists("server.properties"):
            
            with open("server.properties", "r") as f:
                allLines = f.readlines()
                for line in allLines:
                    line = line[line.find("="):]
                    line = line.replace("=", "")
                    settings.append(line.replace("\n", ""))
            f.close()
            print(settings)
            break
                
        else:
            createFile = open("server.properties", "w+")
            createFile.write("servername=\nport=56000\nmaxusers=5")
            createFile.close()
    
def broadcast(msg):
    if msg != "":
        for client in clients:
            try:
                client.sendall(msg.encode())
            except:
                try:
                    client.close()
                    if client in clients: 
                        clients.remove(client)
                except:
                    continue
                


def new_client(clientsocket, addr):
    servernameanddescription = "servernameanddescription/" + settings[0] + "¤" + settings[3] + "¤"
    try:
        clientsocket.send(servernameanddescription.encode())
    except:
        print("Couldn't send servername and description")
        return
    
    while True:
        try:
            msg = clientsocket.recv(1024)
            msg = msg.decode("utf-8")
            if msg:
                if msg.startswith("username/"):
                    username = msg.replace("username/", "")
                    clientsData.append(username)
                    newJoined = "newjoined/" + str(username) + ' joined the server!\n'
                    broadcast(newJoined)
                    
                elif msg.startswith("exit/"):
                    username = msg.replace("exit/", "")
                    clientsData.remove(username)
                    newLeaved = "newjoined/" + str(username) + ' left the server\n'
                    broadcast(newLeaved)
                    
                else:
                    print(msg)
                    broadcast(msg)
                    
        except:
            continue

def accept_clients(s):
    while True:
       if not len(clients) >= int(settings[2]):
           try:
               c, addr = s.accept()  
               clients.append(c)
               print ('Got connection from ' + str(addr))
               try:
                   threading.Thread(target=new_client, args=(c,addr)).start()
               except:
                   print("Could not start thread")

           except:
                print("Could not accept new client")


fileStuff()

s = socket.socket()    
              
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)

if settings[1] != "":
    port = int(settings[1])
else:
    print("no port specified. new port found.")
    port = 0

try:
    s.bind((IPAddr, port))
    print("Port and ip binded")
except:
    print("Could not bind port and ip")
    sys.exit()
 
print("\nWaiting for connection...")
print("IP: " + IPAddr + " Port: " + str(port))

clients = []
clientsData = []
s.listen()

acceptClientsThread = threading.Thread(target=accept_clients, args=(s,))
acceptClientsThread.start()

while True:
    serverInput = input("Server >> ")
    if serverInput == "stop":
        s.close()
        acceptClientsThread.join()
        sys.exit()
    else:
        sendMsg = "Server >> " + serverInput
        broadcast(sendMsg)
