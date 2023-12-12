# Клієнт v1
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Listbox

class ClientGUI:
    def __init__(self, master, host, port):
        self.master = master
        self.host = host
        self.port = port

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_clients = []

        self.create_widgets()
    
    def auto_scroll(self):
        # Викликати цей метод для автоматичного скролінгу
        self.text_area.yview_moveto(1.0)

    def create_widgets(self):
        self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10, expand=True, fill='both')

        self.entry = Entry(self.master, width=50)
        self.entry.pack(padx=10, pady=10, side=tk.LEFT, expand=True, fill='both')

        send_button = Button(self.master, text="Send", command=self.send_message)
        send_button.pack(padx=10, pady=10, side=tk.RIGHT)

        self.connected_clients_listbox = Listbox(self.master)
        self.connected_clients_listbox.pack(padx=10, pady=10, side=tk.RIGHT)

        self.entry.bind("<Return>", lambda event: self.send_message())

        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.host, self.port))
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            print(f"Error connecting to the server: {e}")

    def send_message(self):
        message = self.entry.get()
        if message:
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.auto_scroll()
                self.entry.delete(0, tk.END)  # Clear the entry field after sending
            except Exception as e:
                print(f"Error sending message: {e}")

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break  # Exit the loop if no data is received

                received_message = data.decode('utf-8')
                if received_message.startswith("%Has joined the chat:"):
                    # Handle connected clients list
                    connected_clients = received_message[len("%Has joined the chat:"):].split()
                    self.update_connected_clients(connected_clients)
                else:
                    # Handle regular messages
                    self.text_area.insert(tk.END, received_message + '\n')
                    self.auto_scroll()
            except Exception as e:
                print(f"Error receiving message: {e}")
                break  # Exit the loop in case of an error

# ...
    def update_connected_clients(self, connected_clients):
        self.connected_clients_listbox.delete(0, tk.END)  # Clear the listbox
        for client in connected_clients:
            # Видаляємо квадратні дужки та апострофи
            cleaned_client = client.strip(" []', ")
            # Додаємо очищений елемент до списку
            self.connected_clients_listbox.insert(tk.END, cleaned_client)
# ...


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chat Client")
    
    # Replace '127.0.0.1' and 5555 with your server's host and port
    client_gui = ClientGUI(root, host='127.0.0.1', port=5555)

    root.mainloop()
