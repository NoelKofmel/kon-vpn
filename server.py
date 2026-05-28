import socket
import threading

BUFFER_SIZE = 1024
PORT = 5050
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True

    while connected:
        try:
            data = conn.recv(BUFFER_SIZE)

            if not data:
                break

            message = data.decode(FORMAT)

            print(f"[{addr}] {message}")

            conn.send(f"Echo: {message}".encode(FORMAT))

        except ConnectionResetError:
            print(f"[ERROR] Connection lost with {addr}")
            break

    conn.close()

    print(f"[DISCONNECTED] {addr}")


def start():
    server.listen()

    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))

        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print(f"[STARTING] Server is starting...")

start()
