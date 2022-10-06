# region Libraries

import socket

# endregion



# region Basic Client Functions

def InitializeConnection():
    global clientSocket, serverAdress
    
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAdress = ("localhost", 5016)
    clientSocket.connect(serverAdress)
    print("I'm connected to the server {} on port {}.".format(*serverAdress))

def SendMenssage(message_):
    global clientSocket
    
    clientSocket.sendall(message_.encode())

def ReceiveMessage():
    global clientSocket
    
    messageReceived = None
    while not messageReceived:
        messageReceived = clientSocket.recv(1024)
    return messageReceived.decode()

# endregion



# region App Functions

def CloseConnection():
    global clientSocket
    
    clientSocket.close()

# endregion



# region Global Variables

clientSocket = None
serverAdress = None

closeMessage = "!close"

# endregion 



# region Code

InitializeConnection()
while True:
    messageReceived = ReceiveMessage()
    if messageReceived == closeMessage:
        break
    else:
        response = input(messageReceived)
        SendMenssage(response)
CloseConnection()

# endregion