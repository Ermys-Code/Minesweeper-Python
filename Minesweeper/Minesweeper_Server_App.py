from email import message
import socket
import random



#Basic functions
def Initialize_connection():
    global serverSocket,serverAddress

    serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverAddress=('localhost',5016)
    serverSocket.bind(serverAddress)
    serverSocket.listen()
    print('server {} conneted on port: {}'.format(*serverAddress))

def Accept_client():
    global serverSocket,clientAddress,connection, connectionOpen

    print("waiting for player...")
    while not connection or not clientAddress:
        connection,clientAddress=serverSocket.accept()
    print("Client {} has connected.".format(clientAddress))
    connectionOpen = True

def Send_message(message):
    global connection

    connection.sendall(message.encode())

def Receive_message():
    global connection

    messageReceived=None
    while not messageReceived:
        messageReceived=connection.recv(1024)
    return messageReceived.decode()

def Close_connection():
    global closeConnectionMessage, connection, clientAddress, connectionOpen

    Send_message(closeConnectionMessage)
    connection.close()
    print("Connection with the client {} closed.".format(clientAddress))
    connectionOpen = False
    connection = None
    clientAddress = None



#App functions
def Mines_generator():
    global mineArray, showArray, cellsLeft

    cellsLeft = 0
    mineArray = []
    showArray = []
    for y in range(8):
        newMineArray = []
        newShowArray = []
        for x in range(8):
            number = random.randint(1, 100)
            if number > 0 and number <= 40:
                number = 1
            else:
                number = 0
            newMineArray.append(number)
            newShowArray.append("X")
        mineArray.append(newMineArray)
        showArray.append(newShowArray)
    for array in mineArray:
        for value in array:
            if value == 0:
                cellsLeft += 1

def Array_to_string():
    global showArray, mineArray

    mineString = ""
    for y in range(len(mineArray)):
        for x in range(len(mineArray[y])):
            mineString += str(showArray[y][x]) + " "
        mineString += "\n"
    return mineString

def Main_menu():
    global menu, mainMenuOptions, mainMenuError

    Send_message(mainMenuError + menu)
    mainMenuError = ""
    response = Receive_message()
    if response in mainMenuOptions.keys():
        mainMenuOptions[response]()
    else:
        mainMenuError = "Option no valid\n\n"
        Main_menu()

def Check_sorrownding(y, x):
    mineCounter = 0
    y = y - 1
    x = x - 1
    for i in range(3):
        if y + i == -1 or y + i == len(mineArray):
            continue
        for j in range(3):
            if x + j == -1 or x + j == len(mineArray[0]):
                continue
            if mineArray[y + i][x + j] == 1:
                mineCounter += 1
    return mineCounter

def Depth_first_search(array, y, x):
    global showArray, cellsLeft

    mineCounter = 0
    mineCounter = Check_sorrownding(y, x)
    if mineCounter == 0:
        showArray[y][x] = "-"
        cellsLeft -= 1
    else:
        showArray[y][x] = mineCounter
        cellsLeft -= 1
    if (y - 1) >= 0 and str(showArray[y - 1][x]) == "X" and array[y - 1][x] == 0:
        Depth_first_search(array, y - 1, x)
    if (x + 1) < len(array[0]) and str(showArray[y][x + 1]) == "X" and array[y][x + 1] == 0:
        Depth_first_search(array, y, x + 1)
    if (y + 1) < len(array) and str(showArray[y + 1][x]) == "X" and array[y + 1][x] == 0:
        Depth_first_search(array, y + 1, x)
    if (x - 1) >= 0 and str(showArray[y][x - 1]) == "X" and array[y][x - 1] == 0:
        Depth_first_search(array, y, x -1)

def String_to_coord(string):
    string = string.replace("/", "")
    string = [*string]
    string = [eval(i) for i in string]
    string[0] -= 1
    string[1] -= 1
    return string

def Check_coord(coord):
    global mineArray
    
    coordValue = mineArray[coord[1]][coord[0]]
    return coordValue == 1

def Play_again():
    global playAgainQuestion

    Send_message(playAgainQuestion)
    response = Receive_message()
    return response == "yes"

def Win():
    global winQuestion

    Send_message(winQuestion)
    response = Receive_message()
    return response == "yes"

def GetCoords():
    while True:
        coord = Receive_message()
        coord = String_to_coord(coord)
        if coord[0] < 0 or coord[0] > (len(mineArray[0]) - 1) or coord[1] < 0 or coord[1] > (len(mineArray) - 1):
            message = "Not a valid coord\n\nSelect a valid coord: (x/y) "
            Send_message(message)
        else:
            print(coord)
            print(type(coord))
            return coord

def Minesweeper():
    global mineArray, showArray, cellsLeft, playing

    while True:
        Mines_generator()
        while True:
            if cellsLeft == 0:
                if Win():
                    break
                else:
                    return
            message = "\n" + Array_to_string()
            message += "\n\nSelecct a coord: (x/y) "
            Send_message(message)
            
            coord = GetCoords()

            if Check_coord(coord):
                if Play_again():
                    break
                else:
                    return
            else:
                Depth_first_search(mineArray, coord[1], coord[0])




#Global variables
serverSocket = None
serverAddress = None
clientAddress = None
connection = None

playerCount=1
mineArray = []
showArray = []
connectionOpen = False
cellsLeft = 0
mainMenuError = ""

menu = """
MINESWEEPER

1 - Ready for game
2 - Exit

Select an option: """
closeConnectionMessage = "!close"
playAgainQuestion = "Fail!\n\nDo you want to play again? (yes / no) "
winQuestion = "You win!\n\nDo you want to play again? (yes / no) "

mainMenuOptions = {
    "1" : Minesweeper,
    "2" : Close_connection
}



#Code
Initialize_connection()
while True:
    Accept_client()
    while connectionOpen:
        Main_menu()

