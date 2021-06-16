import requests
import json
import socket

DEST_ADDR = 'http://127.0.0.1:5000/'
USERNAME = 'Peter'
PASSWORD = 'Peter_Enis'
FORMAT = 'utf-8'


def client_register_test():
    response = requests.post(DEST_ADDR + 'Register', {'username': USERNAME})
    print(response.json())
    ID = json.loads(response.json())['id']
    print(ID)
    return ID


def lobby_list_test():
    response = requests.get(DEST_ADDR + 'LobbyList')
    lobby_list_meta = json.loads(response.json())
    print('Lobby count: {} \nLobbies: {}'.format(lobby_list_meta['count'], lobby_list_meta['list']))


def lobby_create_test(name: str, c_id):
    response = requests.put(DEST_ADDR + 'Create', {'name': name, 'username': USERNAME, 'password': PASSWORD, 'client_id': c_id})
    print(response)
    l_id = json.loads(response.json())['id']
    print(l_id)
    return l_id
    # TODO: Username should not be asked here, server should know it


def lobby_join_test(l_id, c_id):
    response = requests.post(DEST_ADDR + 'Lobby_Join/{}'.format(l_id), {'client_id': c_id, 'password': PASSWORD})
    address = json.loads(response.json())['address']

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    answer = s.recv(1024).decode(FORMAT)
    print(answer)
    print(f"{json.loads(answer)['method']} || {json.loads(answer)['data']}")
    s.send(json.dumps({'method': 'init', 'ini': 10}).encode(FORMAT))
    return s


if __name__ == '__main__':
    # REGISTER NEW CLIENT
    client_id = client_register_test()

    lobby_list_test()

    lobby_create_test('Peter\'s Ballerbude', client_id)

    # response = requests.post(DEST_ADDR + 'Logout',{'client_id':ID})  # NOT IMPLEMENTED YET
