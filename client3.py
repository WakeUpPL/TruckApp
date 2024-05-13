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
        self.text_area.yview_moveto(1.0)

    def create_widgets(self):
        self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10, expand=True, fill='both')

        # Перший ряд кнопок
        frame1 = tk.Frame(self.master)
        frame1.pack(side=tk.TOP, padx=10, pady=5)
        button1 = Button(frame1, text="GATT4", command=lambda: self.send_with_user("GATT4"))
        button1.pack(side=tk.LEFT, padx=5)
        button2 = Button(frame1, text="GAT22", command=lambda: self.send_with_user("GAT22"))
        button2.pack(side=tk.LEFT, padx=5)
        button3 = Button(frame1, text="GAT41", command=lambda: self.send_with_user("GAT41"))
        button3.pack(side=tk.LEFT, padx=5)

        # Другий ряд кнопок
        frame2 = tk.Frame(self.master)
        frame2.pack(side=tk.TOP, padx=10, pady=5)
        button4 = Button(frame2, text="Zaladunek", command=lambda: self.send_with_user("#LOAD"))
        button4.pack(side=tk.LEFT, padx=5)
        button5 = Button(frame2, text="END", command=lambda: self.send_with_user("#END"))
        button5.pack(side=tk.LEFT, padx=5)
        button6 = Button(frame2, text="Documents", command=lambda: self.send_with_user("#DOC"))
        button6.pack(side=tk.LEFT, padx=5)

        self.entry = Entry(self.master, width=50)
        self.entry.pack(padx=10, pady=10, side=tk.LEFT, expand=True, fill='both')

        send_button = Button(self.master, text="Send", command=self.send_message)
        send_button.pack(padx=10, pady=10, side=tk.LEFT)

        self.connected_clients_listbox = Listbox(self.master)
        self.connected_clients_listbox.pack(padx=10, pady=10, side=tk.LEFT)

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
                self.entry.delete(0, tk.END)  
            except Exception as e:
                print(f"Error sending message: {e}")

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break  

                received_message = data.decode('utf-8')
                if received_message.startswith("%Has joined the chat:"):
                    connected_clients = received_message[len("%Has joined the chat:"):].split()
                    self.update_connected_clients(connected_clients)
                else:
                    self.text_area.insert(tk.END, received_message + '\n')
                    self.auto_scroll()
            except Exception as e:
                print(f"Error receiving message: {e}")
                break  

    def update_connected_clients(self, connected_clients):
        self.connected_clients_listbox.delete(0, tk.END)  
        for client in connected_clients:
            cleaned_client = client.strip(" []', ")
            self.connected_clients_listbox.insert(tk.END, cleaned_client)

    def send_with_user(self, text):
        selected_index = self.connected_clients_listbox.curselection()
        if selected_index:
            selected_item = self.connected_clients_listbox.get(selected_index)
            message = f"@{selected_item} {text}"
            self.set_entry_text(message)

    def set_entry_text(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, text)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chat Client")
     # host = '91.207.60.55'
    client_gui = ClientGUI(root, host='localhost', port=5555)

    root.mainloop()
