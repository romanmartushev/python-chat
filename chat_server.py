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
    conn.send('Please login by typing: login [username]') # sends a message to the client whose user object is conn
    while True:
            try:
                message = conn.recv(2048)
                if message:

                    for clients in list_of_clients:
                        if clients[0] == conn:
                            sender = clients # Sets the incoming sender

                    recipient = sender # sets the sender as recipient
                    logout = False # sets logout flag to false
                    exit = False # sets exit flag to false

                    command = message.split(' ', 1)[0].rstrip() # grabs the first item from string which is the command

                    if command == 'login':
                        sender[2] = message.split(' ', 1)[1].rstrip() # sets the incoming senders name
                        message_to_send = 'You are logged in as ' + sender[2] # return message to be sent to incloming sender after login

                    elif command == 'list':
                        message_to_send = 'users online:\n' #  add a header to the list so we know these are the users online
                        for c in list_of_clients:
                            if c[2] != '':
                                message_to_send = message_to_send + c[2] + '\n' # adds all the names of everyone currently logged into the chat to a string

                    elif command == 'sendto':
                        if sender[2] == '':
                            message_to_send = 'Please login'
                        elif sender[2] != '':
                            recipient = message.split(' ', 2)[1].rstrip()
                            for clients in list_of_clients:
                                if clients[2] == recipient:
                                    recipient = clients # Sets the outgoing recipient

                            message_to_send = sender[2] + ':'+ message.split(' ', 2)[2].rstrip()

                    elif command == 'logout':
                        logout = True
                        message_to_send = 'client removed'

                    else:
                        exit = True
                        message_to_send = 'EXIT'
                    broadcast(message_to_send,sender,recipient,logout,exit)
                else:
                    remove(conn)
            except:
                continue

def broadcast(message,connection,recipient,logout,exit):
    if logout:
        try:
            connection[0].send(message)
            connection[2] = ''
        except:
            connection[0].close()
            remove(connection)

    elif exit:
        try:
            connection[0].send(message)
            connection[0].close()
            remove(connection)
        except:
            connection[0].close()
            remove(connection)

    elif recipient[0] == connection[0]:
        try:
            connection[0].send(message)
        except:
            connection[0].close()
            remove(connection)
    else:
        try:
            recipient[0].send(message)
        except:
            recipient[0].close()
            remove(recipient)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_clients.append([conn,addr,'']) # maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    print addr[0] + ' connected' # Prints the address of the person who just connected
    start_new_thread(clientthread,(conn,addr))#creates and individual thread for every user that connects

conn.close()
server.close()
