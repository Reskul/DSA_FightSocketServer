import socket
import threading
from client import Client
import json
from json import JSONEncoder

DEBUG = True


class LobbyServer(threading.Thread):
    def __init__(self, l_id, name, owner, password):
        super().__init__()
        self.PORT = 5001 + l_id
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
        print(self.server)

    def client_join(self, client: Client):
        """Used in Thread so achieve non-stopping behaviour."""
        conn, addr = self.server.accept()  # TODO: crashes because of async call, server isnt bound in instance called.
        while addr != client.addr:
            conn.close()  # TODO: Test if this is doing what i want
            conn, addr = self.server.accept()
        client.join_lobby(conn, self.LOBBY_ID)
        conn.send(self.JOIN_MSG)
        conn.flush()
        data = conn.recv(self.MAXLENGTH).decode(self.FORMAT)
        data = json.loads(data)
        if data['method'] == 'init':
            self.clients.append((client, data['ini']))
        else:
            # fehler schmeißen
            pass

        if DEBUG:
            print(self.clients)
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


class LobbySimpEncoder(JSONEncoder):
    def default(self, lobby):
        return lobby.__dict__
