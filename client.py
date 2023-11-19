import socket

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY, 1)
sock.connect(('localhost',10000))

while True:
    #read enter msg

    #send msg on server
    sock.send('Check #1, Check #2, Check #3, Check #4'.encode())

    #takeing msg from server
    data=sock.recv(1024)
    data=data.decode()
    print(data)

    
