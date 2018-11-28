import socket
import select
from thread import *
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8882        # The port used by the server
server.bind((HOST, PORT)) # bind server to the ip at the specified port number
server.listen(5) # listens for 5 active connections.
list_of_clients=[]

def clientthread(conn,addr):
    conn.send("Please Login! bye typing: login [username]") # sends a message to the client whose user object is conn
    while True:
            try:
                message = conn.recv(2048)
                if message:
                    command = message.split(' ', 1)[0].rstrip()

                    if command == 'login':
                        for clients in list_of_clients:
                            if clients[0] == conn:
                                clients[2] = message.split(' ', 1)[1].rstrip()
                    elif command == 'list':
                        message = 'users online: '.join(str(e[2]) for e in list_of_clients)

                    for clients in list_of_clients:
                        if clients[0] == conn and clients[2] == '':
                            message_to_send = "Please login"
                        elif clients[0] == conn and clients[2] != '':
                            message_to_send = "<" + clients[2] + "> " + message
                    print message_to_send
                    broadcast(message_to_send,conn)
                else:
                    remove(conn)
            except:
                continue

def broadcast(message,connection):
    for clients in list_of_clients:
        if clients[0] == connection:
            try:
                clients[0].send(message)
            except:
                clients[0].close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
        print "client removed"

while True:
    conn, addr = server.accept()
    """
    Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains
    the IP address of the client that just connected
    """
    list_of_clients.append([conn,addr,'']) # maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    print addr[0] + " connected" # Prints the address of the person who just connected
    start_new_thread(clientthread,(conn,addr))#creates and individual thread for every user that connects

conn.close()
server.close()
