import socket

PORT = 5000
SERVER = "192.168.0.188"
ADDR = (SERVER, PORT)
DISCONNECT_MSG = "DISCONNECT".encode('utf-8')
ACK_DISCONNECT = "ACKNOWLEDGED DISCONNECT"

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(ADDR)
print("Connected...")
socket.send("Hello World.".encode('utf-8'))
input("Message sent.")
socket.send(DISCONNECT_MSG)
result = socket.recv(1024).decode('utf-8')
if result == ACK_DISCONNECT:
    socket.close()
    input("Disconnected...")
else:
    input("Something went wrong.")


if __name__ == '__main__':
    hello = 1
