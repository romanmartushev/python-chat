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
                print message
            else:
                message = sys.stdin.readline()
                argument = message.split(' ', 1)[0].rstrip()
                checkCommand(argument, message)
                sys.stdout.flush()
    server.close()

def checkCommand(argument, message):
    switcher = {
        'login' : login,
        'list' : list,
        'sendto' : sendto,
        'logout' : logout,
        'exit' : exit
    }
    func = switcher.get(argument,'Invalid argument')
    if func != 'Invalid argument':
        func(message)
    else:
        print func

def login(message):
    server.send(message)
    sys.stdout.write("<You>")
    sys.stdout.write(message)

def list(message):
    server.send(message)
    sys.stdout.write("<You>")
    sys.stdout.write(message)

def sendto(message):
    print 'sendto'

def logout(message):
    server.send('logout')
    sys.stdout.write("<You>")
    sys.stdout.write("logout")

def exit(message):
    server.send('exit')
    sys.stdout.write("<You>")
    sys.stdout.write("exit")

main()
