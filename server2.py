import socket
import threading
import os
from datetime import datetime

def handle_client(client_socket, addr, clients, history_file, nicknames, lock):
    try:
        client_socket.send("Welcome to the chat! \n".encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8')

        with lock:
            nicknames.append(nickname)
            broadcast(f"%Has joined the chat: {nicknames} \n", clients, nicknames)
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            full_message = f"{timestamp} {nickname}: {message}"

            if nickname != "@admin":
                # Non-admin users send messages to @admin
                with lock:
                    admin_socket = find_client_by_nickname("@admin", clients, nicknames)
                if admin_socket:
                    admin_socket.send(f"Private message from {timestamp} {nickname}: {message}".encode('utf-8'))
                else:
                    client_socket.send("Error: Admin not found.".encode('utf-8'))
            elif message.startswith("@"):
                # Admin can send private messages to any user
                recipient, private_message = message.split(" ", 1)
                with lock:
                    recipient_socket = find_client_by_nickname(recipient[1:], clients, nicknames)
                if recipient_socket:
                    recipient_socket.send(f"Private message from {timestamp} {nickname}: {private_message}".encode('utf-8'))
                else:
                    client_socket.send(f"Error: User '{recipient[1:]}' not found.".encode('utf-8'))
            else:
                # Admin broadcasts messages to all clients
                with lock:
                    broadcast(full_message, clients, nicknames)
                    with open(history_file, 'a') as history:
                        history.write(f"{full_message}\n")

    except ConnectionResetError:
        pass
    finally:
        print(f"Connection with {addr} closed.")
        with lock:
            clients.remove(client_socket)
            nicknames.remove(nickname)
            broadcast(f"%Has left the chat: {nickname} \n", clients, nicknames)
            broadcast(f"%Has joined the chat: {nicknames} \n", clients, nicknames)
        client_socket.close()

def broadcast(message, clients, nicknames):
    for client, nickname in zip(clients, nicknames):
        client.send(message.encode('utf-8'))

def find_client_by_nickname(nickname, clients, nicknames):
    for client, name in zip(clients, nicknames):
        if name == nickname:
            return client
    return None

def main():
    host = '127.0.0.1'
    port = 5555
    history_file = 'chat_history.txt'

    if not os.path.exists(history_file):
        with open(history_file, 'w'):
            pass

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"[*] Listening on {host}:{port}")

    clients = []
    nicknames = []
    lock = threading.Lock()

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        clients.append(client)

        client_handler = threading.Thread(target=handle_client, args=(client, addr, clients, history_file, nicknames, lock))
        client_handler.start()

if __name__ == "__main__":
    main()
