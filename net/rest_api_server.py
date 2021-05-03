from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from lobby_server import *
from client import Client
import json
import random

app = Flask(__name__)
api = Api(app)

create_args = reqparse.RequestParser()
create_args.add_argument("name", type=str, help="Lobbyname is required.", required=True)  # quasi objekt parameter, per json transferiert
create_args.add_argument("username", type=str, help="Username is missing.", required=True)
create_args.add_argument("password", type=str, help="Password is missing.")

destroy_args = reqparse.RequestParser()
destroy_args.add_argument("lobby", type=int, help="Lobby ID is required.", required=True)
destroy_args.add_argument("pwd", type=str, help="Password is required.", requireed=True)

client_register_args = reqparse.RequestParser()  # Parser for nearly every client request, containing info about the client itself & stuff
client_register_args.add_argument("username", type=str, help="Human readable username.", required=True)

client_join_args = reqparse.RequestParser()
client_register_args.add_argument("client_id", type=int, help="ID is required to identify client.", required=True)


class LobbyManager:
    """Manages everything about Lobbies."""

    def __init__(self):
        self.lobby_cnt = 0
        self.lobby_nbr = 0
        self.lobbies = []

    def create_new(self, name, pwd, owner):
        """Do some special stuff to create new Lobby."""
        if self.lobby_cnt <= 100:  # TODO: Maybe integrate Database, but for now it should work
            print("I will create a new lobby now.")
            self.lobby_cnt = self.lobby_cnt + 1
            lobby = LobbyServer(self.lobby_nbr, name, owner, pwd)
            lobby.start()
            self.lobbies.append(lobby)
            self.lobby_nbr = self.lobby_nbr + 1
            return LobbySimplified(lobby)
        else:
            print("No lobby slots available.")  # TODO: remove unnecessary limitation

    def join_lobby(self, l_id, client: Client):
        pass  # TODO: Join mechanism

    def check_for_lobby(self, l_id) -> bool:
        """Ask Database/Manager for lobby with l_id"""
        for l in self.lobbies:
            if l.LOBBY_ID == l_id:
                return True
        return False

    def get_full_lobby_list(self):
        """Ask Database for full List of lobbies"""
        simp_lobbies = []
        for l in self.lobbies:
            simp_lobbies.append(LobbySimplified(l))
        return simp_lobbies

    def destroy_lobby(self, l_id, pwd):
        """Removes a lobby from the List."""
        for l in self.lobbies:
            if l_id == l.LOBBY_ID and pwd == l.PWD:
                self.lobbies.remove(l)
                self.lobby_cnt = self.lobby_cnt - 1
                break


class ClientManager:
    """Manages the Clients."""

    def __init__(self):
        self.client_cnt = 0
        self.client_nbr = 0
        self.clients = []
        self.EMPTYCLIENT = Client('0.0.0.0', -1)

    def new_client(self, addr, name) -> Client:
        if self.client_cnt < 1024:
            self.client_cnt = self.client_cnt + 1
            client = Client(addr, self.client_nbr)
            client.clear_name = name
            self.client_nbr = self.client_nbr + 1
            return client

    def get_client(self, c_id) -> Client:
        for cl in self.clients:
            if cl.c_id == c_id:
                return cl
        return self.EMPTYCLIENT


c_mngr = ClientManager()
l_mngr = LobbyManager()


class Register(Resource):
    def connect(self):
        args = client_register_args.parse_args()
        addr = request.remote_addr
        client = c_mngr.new_client(addr, args["username"])  # TODO: think about good id system
        return json.dumps({'id': client.c_id})


class LobbyList(Resource):
    def get(self):
        """Clients can get information about already existing lobbies."""
        return json.dumps({"count": l_mngr.lobby_cnt,
                           "list": l_mngr.get_full_lobby_list()})


class LobbyCreate(Resource):
    def put(self):
        """Used to put a new lobby in the lobby system"""
        args = create_args.parse_args()
        lobby = l_mngr.create_new(args["name"], args["password"], args["username"])
        return json.dumps({"id": lobby.LOBBY_ID})


class LobbyDestroy(Resource):
    def delete(self):
        """receives Destroy call from lobby"""
        args = destroy_args.parse_args()
        l_mngr.destroy_lobby(args["lobby"], args["pwd"])
        return json.dumps({"data": True})


class ClientHelper(Resource):
    def get(self, l_id):
        """Get info about a lobby, for example if its full or playing or stuff"""
        return {"data": {
            "lobby_id": l_id,
            "lobby_meta": {"player_count": 1,
                           "lobby_name": "Peters Hütte"}
        }}

    def post(self, l_id):
        """Player-Clients use this Method to post their will to join a specific lobby"""
        args = client_join_args.parse_args()
        c_id = args['client_id']
        client = c_mngr.get_client(c_id)
        if l_mngr.check_for_lobby(l_id):
            l_mngr.join_lobby(l_id, client)
        else:
            return json.dumps({'data': False, 'msg': "No such Lobby."})


api.add_resource(Register, "/Register")
api.add_resource(LobbyDestroy, "/LobbyDestroy")
api.add_resource(LobbyList, "/LobbyList")
api.add_resource(LobbyCreate, "/Create/<string:Name>/<string:Owner>/<string:Password>")
api.add_resource(ClientHelper, "/LobbyInfo/<int:l_id>")

if __name__ == '__main__':
    app.run(debug=True)
