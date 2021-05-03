class Client:
    def __init__(self, addr, c_id):
        self.clear_name = None
        self.conn = None
        self.addr = addr
        self.c_id = c_id
        self.lobby = None

    def __repr__(self):
        if self.lobby is None:
            return f"ID:{self.c_id}|ADDR:{self.addr}"
        else:
            return f"ID:{self.c_id}|ADDR:{self.addr}|LOBBY_ID:{self.lobby}"

    def join_lobby(self, conn, lobby_id):
        self.conn = conn
        self.lobby = lobby_id
