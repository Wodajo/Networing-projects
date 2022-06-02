from socket import *
import os
import sys
import threading

serverPort = 5050

OS = sys.platform
if OS == "win32":
    serverName = gethostbyname(gethostname())  # serverName could be a hostname (automatically resolved with DNS lookup) or IP address
    # I want it to be server IP
    # This "automatic" IP determination might not work properly when many network adapters
elif OS == "linux":
    serverName = str(os.popen('hostname -I').read().strip())  # I find it more reliable than gethostbyname() on linux, maybe wrongly
else:
    print("Unknown OS")
    serverName = input("IP address of server: ")

while True:
    print(f"You current IP address of the server is {serverName}")
    dec1 = input("Do you want to change IP address? [y/n]: ")
    if dec1.lower().strip() == "y":
        serverName = input("IP address of server: ")
        break
    elif dec1.lower().strip() == "n":
        break
    else:
        pass

serverAddress = (serverName, serverPort)  # serverAddress must be a tuple

HEADER = 64  # First msg of the client to the server is going to be a header of fixed length (64 bytes)
# It will bring info about how big will be next message in bytes (for recv() method)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

serverSocket = socket(AF_INET, SOCK_STREAM)  # AF_INET -> IPv4, SOCK_STREAM -> TCP
# If I'd type "import socket" instead "from socket import *" at the begginig, I should use:
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind(serverAddress)  # Binds/ assigns port to the welcoming socket. Here the three way handshake begins (but not bytes transfer)

def handle_client(connectionSocket, clientAddress):  # for  all (threaded) communication between clients and server
    print(f"[NEW CONNECTION] {clientAddress} connected")

    connected = True
    while connected:
        msg_length = connectionSocket.recv(HEADER).decode(FORMAT)  # Parameter is how many bytes reply is going to have. | Blocking code
        # First we wait for header to tell how big the actual msg is
        if msg_length:  # There exist "blank" messages. We don't want them to mess with int() casting below
            msg_length = int(msg_length)
            msg = connectionSocket.recv(msg_length).decode(FORMAT)  # actual msg
            if msg == DISCONNECT_MESSAGE:  # If client send DISCONNECT_MESSAGE the connectionSocket will be closed
                connected = False

            print(f"[{clientAddress}] {msg}")
            connectionSocket.send("Msg received".encode(FORMAT))

    connectionSocket.close()


def start():
    serverSocket.listen()  # listen for TCP connections. Parameter is max. nr. of  queued connections (at least 1)
    print(f"[LISTENING] Server is listening on {serverName}")
    while True:
        connectionSocket, clientAddress = serverSocket.accept()  # accept() creates connection socket dedicated to this particular client. Completing handshake. | Blocking code
        # clientAddress (like serverAddress) contains both IP address and port number
        thread = threading.Thread(target=handle_client, args=(connectionSocket, clientAddress))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()