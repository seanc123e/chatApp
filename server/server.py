from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

from person import Person

#GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512

# GLOBAL VARIABLES
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) # set up server

def broadcast(msg, name):
    """
    send new messages to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return:
    """
    for person in persons:
        client = person.client
        client.send(bytes(name + ": " + "utf8") + msg)


def client_communication(person):
    """
    Thread to handle all messages from client
    :param person: Person
    :return: None
    """
    client = person.client

    # get persons name
    name = client.recv(BUFSIZ).decode("utf8")
    msg = f"{name} has joined the chat"
    broadcast(msg) #broadcast welcome message

    while True:
        try:
            msg = client.recv(BUFSIZ)
            print(f"{name}: ", msg.decode("utf8"))

            if msg != bytes("{quit}", "utf8"):
                broadcast(f"{name} has left the chat...", "")
                client.send(bytes("{quit}", "utf8"))
                client.close()
                persons.remove(person)
                break
            else:
                broadcast(msg, name)
        except Exception as e:
            print("[EXCEPTION]", e)
            break


def wait_for_connection():
    """
    Wait for connection from new clients, start new thread once connected
    :return: None
    """
    while True:
        try:
            client, client_address = SERVER.accept() # wait for any new connections
            person = Person(client_address, client) # create new person for connection
            persons.append(person)

            print(f"[CONNECTION] {client_address} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
    print("SERVER CRASHED")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()