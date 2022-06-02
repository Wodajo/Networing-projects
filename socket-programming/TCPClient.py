from socket import *

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
serverPort = 5050
while True:
    try:
        serverName = str(input("IP address or hostname of the server: "))
        break
    except ValueError as ex:
        print(f"Error {ex}")
    except:
        print("Sorry")
serverAddress = (serverName, serverPort)

clientSocket = socket(AF_INET, SOCK_STREAM)
# We're NOT specifying the port number of the client socket (like in UDP), OS do it for us
clientSocket.connect(serverAddress) # Initiates TCP connection with given IP and port. Three-way handshake begins!


def send(msg):
    message = msg.encode(FORMAT)  # Properly encoded message
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)  # Properly encoded size of message
    send_length += b' ' * (HEADER - len(send_length))  # Properly encoded size of message with spaces up to 64 bytes
    clientSocket.send(send_length)
    clientSocket.send(message)
    print(clientSocket.recv(2048).decode(FORMAT))  # Here could be the same mechanizm as with HEADER to the server, but I'm lazy

send("Hello World!")
input()
send("Hello Mom&Dad!")
input()
send("Hello Everyone!")

send("Bye!")
send("!DISCONNECT")