#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()   # client_adress is ip and port
        print("client {}:{} has connected with server".format(client_address[0], client_address[1]))
        #client.send(bytes("Welcome to Battleships! Please type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf8")
    #welcome = "Welcome {}! type 'quit' to exit".format(name)

    if players[0] is None:
        index = 0
        client.send(bytes("welcome player1 ","utf8"))
        print("welcome player1")
        players[0] = name
    elif players[1] is None:
        index = 1
        client.send(bytes("welcome player2 ","utf8"))
        print("welcome player2")
        players[1] = name

    broadcast("player{} ({}) has joined the chat!".format(index+1, name), "server:")
    #broadcast(bytes(msg, "utf8"))
    clients[client] = name
    if players[0] is not None and players[1] is not None:
        broadcast("may the game begin!", "server:")

    while True:
        msg = client.recv(BUFSIZ)  # msg is in byte format
        #create string:
        message = "".join([chr(i) for i in msg])

        #if msg != bytes("quit", "utf8"):
        #    broadcast(msg, "player{} ({}): ".format(index+1,name))#, "utf8")
        #else:
        if message == "quit":
            client.send(bytes("quit", "utf8"))
            client.close()
            del clients[client]
            broadcast("player{}({}) has left the chat".format(index+1, name), "server:")   # , "utf8"))
            break
        if message.lower()=="a2" and Game.turn % 2 == index:
            broadcast("mfires at A2", "player{}({})".format(index+1, name))
            Game.turn += 1
            broadcast("turn {}. It is your turn, player{}".format(Game.turn, index+1))
        else:
            broadcast(message, "player{} ({}):".format(index+1,name))



def broadcast(msg, prefix=""):    # prefix tells who is sending the message.
    """Broadcasts a message to all the clients. converts msg to bytes if necessary"""
    msg2 = msg if isinstance(msg, bytes) else bytes(msg, 'utf8')
    for sock in clients:
        #sock.send(bytes(prefix, "utf8") + msg)
        #print("message:", msg, type(msg))
        #print("prefix:", prefix)
        sock.send(bytes(prefix, "utf8") + msg2)

class Game:
    turn = 1


players = [None, None]
clients = {}
addresses = {}


HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()