import socket
import threading
from net.client import Client


class WelcomeServer:
    def __init__(self):
        self.PORT = 5000
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.MAXLENGTH = 1024
        self.DISCONNECT_MSG = "DISCONNECT"
        self.ACK_DISCONNECT = "ACKNOWLEDGED DISCONNECT"
        self.FORMAT = 'utf-8'
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        print(f"[STARTING] My Address is: {self.SERVER}")
        self.client_handler = ClientHandler()
        self.listen()

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            msg = conn.recv(self.MAXLENGTH)
            msg = msg.decode(self.FORMAT)
            print(f"[{addr}]: {msg}")
            if msg == self.DISCONNECT_MSG:
                connected = False
                print(f"[{addr}] Disconnected.")
                conn.send(self.ACK_DISCONNECT.encode(self.FORMAT))
            else:
                conn.send(f"[ECHO][200]: {msg}\n".encode(self.FORMAT))
        conn.close()

    def listen(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            self.client_handler.register_new(conn, addr)
            thread = threading.Thread(target=WelcomeServer.handle_client, args=(self, conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


class LobbyHandler:
    def __init__(self):
        self.lobbies = []
        self.next_id = 1

    def register_new(self, conn, addr):
        self.lobbies.append(Client(conn, addr, self.next_id))
        self.next_id = self.next_id + 1  # well.. this might work but could be better


class ClientHandler:
    def __init__(self):
        self.clients = []
        self.next_id = 1

    def register_new(self, conn, addr):
        self.clients.append(Client(conn, addr, self.next_id))
        self.next_id = self.next_id + 1  # well.. this might work but could be better


if __name__ == '__main__':
    server = WelcomeServer()
