import socket
import threading
from client import Client
import json


class LobbyServer(threading.Thread):
    def __init__(self, l_id, name, owner, password):
        super().__init__()
        self.PORT = 5000 + l_id
        self.LOBBY_ID = l_id
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.MAXLENGTH = 1024
        self.FORMAT = 'utf-8'
        self.JOIN_MSG = json.dumps({'method': 'welcome', 'data': 'join success'})
        self.clients = []
        self.server = None
        self.STATUS = True  # 'WAIT'==True 'INGAME'==False

        # game-logic relevant info
        self.NAME = name
        self.OWNR = owner
        self.PWD = password

    def run(self) -> None:
        super().run()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.server.listen()

    def client_join(self, client: Client):
        """Used in Thread so achieve non-stopping behaviour."""
        conn, addr = self.server.accept()
        while addr != client.addr:
            conn, addr = self.server.accept()
        client.join_lobby(conn, self.LOBBY_ID)
        conn.send(self.JOIN_MSG)
        data = conn.recv(self.MAXLENGTH).decode(self.FORMAT)
        data = json.loads(data)
        if data['method'] == 'init':
            self.clients.append((client, data['ini']))
        else:
            # fehler schmeißen
            pass

        # self.clients.append((client, threading.Thread(target=LobbyServer.handle_client, args={self, conn, client})))

    def client_leave(self):
        """Handles The Client leaving the lobby."""

        pass


class LobbySimplified:
    def __init__(self, lobby: LobbyServer):
        self.NAME = lobby.NAME
        self.OWNER = lobby.OWNR
        self.PWD = lobby.PWD
        self.USER_CNT = len(lobby.clients)
        self.LOBBY_ID = lobby.LOBBY_ID
        self.PORT = lobby.PORT
