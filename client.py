import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8882        # The port used by the server
server.connect((HOST, PORT))

def main():

    while True:
        sockets_list = [sys.stdin, server]
        read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048)
                if message.rstrip() == 'EXIT':
                    return 0;
                else:
                    print message
            else:
                message = sys.stdin.readline()
                argument = message.split(' ', 1)[0].rstrip()
                checkCommand(argument, message)
                sys.stdout.flush()
    server.close()
    print 'You have exited.'

def checkCommand(argument, message):
    switcher = {
        'login' : login,
        'list' : list,
        'sendto' : sendto,
        'logout' : logout,
        'exit' : exit,
        'help' : help
    }
    func = switcher.get(argument,'Invalid argument')
    if func != 'Invalid argument':
        func(message)
    else:
        print func

def login(message):
    if len(message.split(' ', 1)) == 2:
        name = message.split(' ', 1)[1].rstrip()
        if ' ' in name or len(name) > 20:
            print 'Bad username'
        else:
            server.send(message)
    else:
        print 'Bad username'

def list(message):
    list = message.split(' ', 1)
    if len(list) > 1:
        print 'Invalid command'
    else:
        server.send(message)

def sendto(message):
    list = message.split(' ', 2)
    if len(list) != 3 or len(list[1]) > 20:
        print 'Bad username'
    elif len(list[2]) > 65535:
        print 'Bad message'
    else:
        server.send(message)

def logout(message):
    list = message.split(' ', 1)
    if len(list) > 1:
        print 'Invalid command'
    else:
        server.send(message)

def exit(message):
    list = message.split(' ', 1)
    if len(list) > 1:
        print 'Invalid command'
    else:
        server.send(message)

def help(message):
    print 'Commands:'
    print 'login [username] # this command allows you to login to the chat'
    print 'list # allows you to list the users currently online'
    print 'sendto [username] [message] # allows you to send a message to a currently logged in user'
    print 'logout # logs you out of the chat room but you are still allowed to login and list'
    print 'exit # logs you out, closes your connection and closes the chat program'


main()
