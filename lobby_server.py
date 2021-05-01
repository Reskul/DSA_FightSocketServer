import socket
import threading
from socketserver import Client


class LobbyServer(threading.Thread):
    def __init__(self, l_id):
        super().__init__()
        self.PORT = 5000 + l_id
        self.LOBBY_ID = l_id
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.MAXLENGTH = 1024
        self.FORMAT = 'utf-8'
        self.clients = []
        self.server = None

    def run(self) -> None:
        super().run()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.server.listen()

    def client_join(self, client: Client):
        conn, addr = self.server.accept()
        while addr != client.addr:
            conn, addr = self.server.accept()
        self.clients.append((client, threading.Thread(target=LobbyServer.handle_client, args={self, conn, client})))

    def client_leave(self):
        pass

    def handle_client(self, conn, client):
        print(f"[JOINED LOBBY] {client.addr} joined.")

        while client.lobby is not None:
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
